from base58 import b58encode
from contextlib import contextmanager
from enum import IntEnum
from typing import Generator

import pywaves.crypto as pwcrypto

from ragger.backend.interface import BackendInterface, RAPDU
from ragger.utils import split_message


class INS(IntEnum):
    INS_SIGN = 0x02
    INS_GET_PUBLIC_KEY = 0x04
    INS_GET_APP_CONFIGURATION = 0x06


CLA = 0x80

P1_NON_CONFIRM = 0x00  # Don't show address confirmation
P1_CONFIRM = 0x01  # Show address confirmation

P1_MORE = 0x00  # More bytes coming
P1_LAST = 0x80  # End of Bytes to Sign (finalize)

MAX_CHUNK_SIZE = 123  # 128 - 5 service bytes

STATUS_OK = 0x9000


class ErrorType:
    SW_USER_CANCELLED = 0x9100
    SW_DEPRECATED_SIGN_PROTOCOL = 0x9102
    SW_INCORRECT_PRECISION_VALUE = 0x9103
    SW_INCORRECT_TRANSACTION_TYPE_VERSION = 0x9104
    SW_PROTOBUF_DECODING_FAILED = 0x9105
    SW_BYTE_DECODING_FAILED = 0x9106
    SW_CONDITIONS_NOT_SATISFIED = 0x6985
    SW_DEVICE_IS_LOCKED = 0x6986
    SW_BUFFER_OVERFLOW = 0x6990
    SW_INCORRECT_P1_P2 = 0x6A86
    SW_INS_NOT_SUPPORTED = 0x6D00
    SW_CLA_NOT_SUPPORTED = 0x6E00
    SW_SECURITY_STATUS_NOT_SATISFIED = 0x6982


class WavesClient:
    def __init__(self, backend: BackendInterface):
        self._backend = backend

    def send_get_app_configuration(self) -> (bool, (int, int, int)):
        rapdu: RAPDU = self._backend.exchange(CLA, INS.INS_GET_APP_CONFIGURATION, 0, 0, b"")
        response = rapdu.data
        # response = LEDGER_MAJOR_VERSION (1) ||
        #            LEDGER_MINOR_VERSION (1) ||
        #            LEDGER_PATCH_VERSION (1)
        assert len(response) == 3

        major = int(response[0])
        minor = int(response[1])
        patch = int(response[2])
        return (major, minor, patch)

    def compute_adress_from_public_key(self, public_key: bytes, chain_id: str) -> str:
        unhashedAddress = chr(1) + chain_id + pwcrypto.hashChain(public_key)[:20]
        addressHash = pwcrypto.hashChain(pwcrypto.str2bytes(unhashedAddress))[0:4]
        address = b58encode(pwcrypto.str2bytes(unhashedAddress + addressHash))
        return address

    def parse_get_public_key_response(self, response: bytes, chain_id: str) -> (bytes, str, bytes):
        # response = public_key (32) ||
        #            address (35)
        assert len(response) == 67
        public_key: bytes = response[:32]
        address: str = response[32:32+35].decode("ascii")

        assert self.compute_adress_from_public_key(public_key, chain_id) == address

        return public_key, address

    def send_get_public_key_non_confirm(self, chain_id: str,
                                        derivation_path: bytes) -> RAPDU:
        p1 = P1_NON_CONFIRM
        p2 = ord(chain_id)
        return self._backend.exchange(CLA, INS.INS_GET_PUBLIC_KEY,
                                      p1, p2, derivation_path)

    @contextmanager
    def send_async_get_public_key_confirm(self, chain_id: str,
                                          derivation_path: bytes) -> Generator[None, None, None]:
        p1 = P1_CONFIRM
        p2 = ord(chain_id)
        with self._backend.exchange_async(CLA, INS.INS_GET_PUBLIC_KEY,
                                          p1, p2, derivation_path):
            yield

    def _send_sign_message(self, message: bytes, last: bool, chain_id: str) -> RAPDU:
        if last:
            p1 = P1_LAST
        else:
            p1 = P1_MORE
        p2 = ord(chain_id)
        return self._backend.exchange(CLA, INS.INS_SIGN, p1, p2, message)

    @contextmanager
    def _send_async_sign_message(self, message: bytes,
                                 last: bool, chain_id: str) -> Generator[None, None, None]:
        if last:
            p1 = P1_LAST
        else:
            p1 = P1_MORE
        p2 = ord(chain_id)
        with self._backend.exchange_async(CLA, INS.INS_SIGN, p1, p2, message):
            yield

    def send_async_sign_message(self,
                                chain_id: str,
                                derivation_path: bytes,
                                message: bytes) -> Generator[None, None, None]:
        messages = split_message(derivation_path + message, MAX_CHUNK_SIZE)

        if len(messages) > 1:
            for m in messages[:-1]:
                self._send_sign_message(m, False, chain_id)

        return self._send_async_sign_message(messages[-1], True, chain_id)

    def get_async_response(self) -> RAPDU:
        return self._backend.last_async_response
