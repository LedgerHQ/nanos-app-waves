from pathlib import Path

from ragger.backend import SpeculosBackend
from ragger.backend.interface import RAPDU, RaisePolicy
from ragger.navigator import NavInsID, NavIns
from ragger.utils import pack_derivation_path

from apps.waves import WavesClient, ErrorType
from apps.waves_transaction_builder import TransfertBytesTransaction


TESTS_ROOT_DIR = Path(__file__).parent

TESTNET_CHAIN_ID = 'T'
MAINNET_CHAIN_ID = 'W'

# Proposed EOS derivation paths for tests ###
# Waves app doesn't expect the leading length byte, but to have exactly
# 20 bytes (e.g. 5 derivation of 4 bytes)
WAVES_PATH = pack_derivation_path("m/44'/5741564'/0'/0'/1'")[1:]

SPECULOS_EXPECTED_PUBLIC_KEY = "115b3612c318a37ba6cd32cbf0126e77"\
                               "3f0d21218ef187aa83a7c02a68778244"

SPECULOS_EXPECTED_ADDRESS = "3P3iWa95nuathZn7EtFHxVBafrvMvPTkGPs"


def get_review_instructions(num_screen_skip):
    instructions = [NavIns(NavInsID.RIGHT_CLICK)] * num_screen_skip
    instructions.append(NavIns(NavInsID.BOTH_CLICK))
    return instructions


def test_waves_mainmenu(backend, test_name, navigator):
    waves = WavesClient(backend)

    # Get appversion
    version = waves.send_get_app_configuration()
    assert version == (1, 1, 4)

    # Navigate in the main menu and the setting menu
    # Change the "data_allowed parameter" value
    instructions = [
        NavIns(NavInsID.RIGHT_CLICK),
        NavIns(NavInsID.RIGHT_CLICK),
        NavIns(NavInsID.RIGHT_CLICK),
    ]
    navigator.navigate_and_compare(TESTS_ROOT_DIR, test_name, instructions)


def check_get_public_key_resp(client, public_key, address):
    if isinstance(client, SpeculosBackend):
        # Check against nominal Speculos seed expected results
        assert public_key.hex() == SPECULOS_EXPECTED_PUBLIC_KEY
        assert address == SPECULOS_EXPECTED_ADDRESS


def test_waves_get_public_key_non_confirm(backend):
    waves = WavesClient(backend)

    rapdu: RAPDU = waves.send_get_public_key_non_confirm(MAINNET_CHAIN_ID, WAVES_PATH)
    public_key, address = waves.parse_get_public_key_response(rapdu.data, MAINNET_CHAIN_ID)
    check_get_public_key_resp(backend, public_key, address)


def test_waves_get_public_key_confirm(test_name, backend, firmware, navigator):
    waves = WavesClient(backend)
    if firmware.device == "nanos":
        instructions = get_review_instructions(4)
    else:
        instructions = get_review_instructions(2)
    with waves.send_async_get_public_key_confirm(MAINNET_CHAIN_ID, WAVES_PATH):
        navigator.navigate_and_compare(TESTS_ROOT_DIR,
                                       test_name,
                                       instructions)
    rapdu: RAPDU = waves.get_async_response()
    public_key, address = waves.parse_get_public_key_response(rapdu.data, MAINNET_CHAIN_ID)
    check_get_public_key_resp(backend, public_key, address)


def test_waves_get_public_key_confirm_refused(test_name, backend, firmware, navigator):
    waves = WavesClient(backend)
    if firmware.device == "nanos":
        instructions = get_review_instructions(5)
    else:
        instructions = get_review_instructions(3)
    with waves.send_async_get_public_key_confirm(MAINNET_CHAIN_ID, WAVES_PATH):
        backend.raise_policy = RaisePolicy.RAISE_NOTHING
        navigator.navigate_and_compare(TESTS_ROOT_DIR,
                                       test_name,
                                       instructions)
    rapdu: RAPDU = waves.get_async_response()
    assert rapdu.status == ErrorType.SW_USER_CANCELLED
    assert len(rapdu.data) == 0


def test_waves_transaction_ok(test_name, backend, navigator):
    data = {
        "publicKey": '4ovEU8YpbHTurwzw8CDZaCD7m6LpyMTC4nrJcgDHb4Jh',
        "asset": '9gqcTyupiDWuogWhKv8G3EMwjMaobkw9Lpys4EY2F62t',
        "timestamp": 1526477921829,
        "amount": 100000000,
        "txFee": 100000,
        "recipient": '3P3iWa95nuathZn7EtFHxVBafrvMvPTkGPs',
        "attachment": 'privet'
    }
    message = TransfertBytesTransaction().encode(data)
    waves = WavesClient(backend)
    instructions = get_review_instructions(9)
    with waves.send_async_sign_message(MAINNET_CHAIN_ID, WAVES_PATH, message):
        navigator.navigate_and_compare(TESTS_ROOT_DIR,
                                       test_name,
                                       instructions)
    rapdu: RAPDU = waves.get_async_response()
    # not implemented
    # waves.verify_signature(WAVES_PATH, signing_digest, rapdu.data)
