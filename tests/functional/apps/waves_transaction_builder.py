from base58 import b58decode
from struct import pack

import pywaves.crypto as pwcrypto


class TransfertBytesTransaction:
    def encode_transaction_data(self, data_type, data_version, transaction_data):
        # data type: byte ignored by the app
        binary_data = pack("B", data_type)

        # data version: byte skipped if header data version == 2, else not expected
        if data_version == 2:
            binary_data += pack("B", data_version)

        binary_data += b58decode(transaction_data["publicKey"])
        if "asset" in transaction_data:
            binary_data += pack("B", 1)
            binary_data += b58decode(transaction_data["asset"])
        else:
            binary_data += pack("B", 0)

        if "feeAsset" in transaction_data:
            binary_data += pack("B", 1)
            binary_data += b58decode(transaction_data["feeAsset"])
        else:
            binary_data += pack("B", 0)

        binary_data += pack(">Q", transaction_data["timestamp"])

        binary_data += pack(">Q", transaction_data["amount"])

        binary_data += pack(">Q", transaction_data["txFee"])

        binary_data += b58decode(transaction_data["recipient"])

        attachment = transaction_data.get("attachment", "")
        binary_data += pack(">H", len(attachment))
        binary_data += pwcrypto.str2bytes(attachment)

        return binary_data

    def encode(self, transaction_data):
        data_type = 4
        data_version = 2

        # tx amount asset decimals
        binary_data = pack("B", 8)
        # fee amount asset decimals
        binary_data += pack("B", 8)

        # data type
        binary_data += pack("B", data_type)
        # data version
        binary_data += pack("B", data_version)

        binary_transaction_data = self.encode_transaction_data(data_type, data_version, transaction_data)
        # data length
        binary_data += pack(">I", len(binary_transaction_data))
        # data
        binary_data += binary_transaction_data
        # WARNING: this hack is necessary so that the transaction is processed
        binary_data += binary_transaction_data

        return binary_data
