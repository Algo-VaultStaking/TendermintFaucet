import re
import os
import secrets
from logger import log, raw_audit_log
from comdexpy import Transaction
import requests
import json


def valid_address(address):
    if re.search('comdex1[0-9a-zA-Z]{38}', address):
        return True
    return False


# Send a transaction to the requestor
def send_testnet_transaction(network: str, address: str, tokens: float, guild_id: int):
    nonce = get_nonce(guild_id, "comdex", network)
    tokens = int(tokens*1000000)

    if network == "mainnet":
        account = 40796
        url = 'https://comdex-rpc.polkachu.com'
        chain_id = "comdex-1"

    elif network == "testnet":
        account = 126
        url = "https://comets.rpc.comdex.one"
        chain_id = "comets-test"

    elif network == "devnet":
        account = 0
        url = 'https://test-rpc.comdex.one'
        chain_id = "test-1"

    else:
        return False

    tx = Transaction(
        privkey=bytes.fromhex(secrets.get_faucet_key(guild_id)),
        account_num=account,
        sequence=nonce,
        fee=2000,
        gas=80000,
        memo="",
        chain_id=chain_id,
        sync_mode="broadcast_tx_sync",
    )

    tx.add_transfer(recipient=address, amount=tokens)
    pushable_tx = tx.get_pushable()
    response = requests.post(url, data=pushable_tx, verify=False)
    print(response.text)
    response = json.loads(response.text)

    try:
        if response['result']['code'] == 0:
            log("Sent testnet transaction to " + address)
            update_nonce(guild_id, "comdex", network, nonce)
            return response['result']['hash']
        else:
            log("Failed to send to " + address)
            return False
    except:
        log("Failed to send to " + address)
        return False


def get_nonce(guild_id: int, chain: str, network: str):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "nonce/" + str(guild_id) + "_" + str(chain) + "_" + network + ".txt")
    f = open(filename, "r")
    nonce = int(f.readline())
    f.close()
    return nonce


def update_nonce(guild_id: int, chain: str, network: str, nonce: int):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "nonce/" + str(guild_id) + "_" + str(chain) + "_" + network + ".txt")
    f = open(filename, "w")
    f.write(str(nonce + 1))
    f.close()


# Get address balance
def get_address_balance(address: str, network: str):
    if network == "mainnet":
        url = "https://rest.comdex.one/cosmos/bank/v1beta1/balances/" + address

    elif network == "testnet":
        url = "https://comets.rest.comdex.one/cosmos/bank/v1beta1/balances/" + address

    elif network == "devnet":
        url = "https://test-rest.comdex.one/cosmos/bank/v1beta1/balances/" + address
    else:
        # default to devnet
        url = "https://test-rest.comdex.one/cosmos/bank/v1beta1/balances/" + address

    try:

        response = requests.get(url, verify=False)
        response = float(json.loads(response.text)['balances'][0]['amount'])/1000000.00
    except Exception as e:
        print(e)
        response = 0.0
    return response


def get_testnet_faucet_balance(guild_id: int):
    address = secrets.get_comdex_faucet_address(guild_id)
    return get_address_balance(address, "testnet")


def get_devnet_faucet_balance(guild_id: int):
    address = secrets.get_comdex_faucet_address(guild_id)
    return get_address_balance(address, "devnet")


# send_testnet_transaction("mainnet", "comdex1zy7uuu6cd5fde3uunlh5l40jjf24ypd6sy9ej4", 1000000, 890929797318967416)  # mainnet
# send_testnet_transaction("testnet", "comdex1zy7uuu6cd5fde3uunlh5l40jjf24ypd6sy9ej4", 1000000, 890929797318967416)  # testnet
# send_testnet_transaction("devnet", "comdex1x7xkvflswrxnkwd42t55jxl9hkhtnnlt43dqs3", 1000000, 890929797318967416)  # devnet
