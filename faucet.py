import re
import os

import secrets
from logger import log
from tendermintwallet import Transaction
import requests
import json
import models


# Send a transaction to the requestor
def send_transaction(chain: str, network: str, address: str, tokens: float, guild_id: int):
    info = models.get_transaction_details(chain, network)

    sequence = int(json.loads(requests.get(info['sequence_url'] + secrets.get_faucet_address(chain, guild_id)).text)["result"]["value"]["sequence"])
    tokens = int(tokens * 1000000)

    tx = Transaction(
        privkey=bytes.fromhex(secrets.get_faucet_key(guild_id)),
        account_num=models.get_faucet_account_num(chain, network, guild_id),
        sequence=sequence,
        fee=5000,
        gas=200000,
        fee_denom=info['denom'],
        memo="",
        chain_id=info['chain_id'],
        sync_mode="broadcast_tx_sync",
    )

    tx.add_transfer(recipient=address, amount=tokens, denom=info['denom'], chain=chain)
    pushable_tx = tx.get_pushable()
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }

    response = requests.post(info['rpc_url'], data=pushable_tx, headers=headers)  # verify=False
    print(response.text)
    response = json.loads(response.text)

    try:
        if response['result']['code'] == 0:
            log("Sent testnet transaction to " + address)
            update_nonce(chain, network, sequence, guild_id)
            return response['result']['hash']
        elif response['result']['code'] == 7:
            log("Invalid address: " + address)
            return response['result']['log']
        elif response['result']['code'] == 32:
            log("Invalid sequence: " + address)
            return "The faucet is working on a backlog of transactions. Please try again shortly."
        elif response['result']['code'] == -32603:
            log("'Internal error, tx already exists in cache'")
            return "Tx already exists in cache."
        else:
            log("Failed to send to " + address)
            return "There was an issue sending funds. cc: <@712863455467667526>"
    except Exception as e:
        log(f"There was an exception:\n{str(e)}\n{str(response)}")
        log(f"code: {response['result']['code']}")
        return "We ran into a problem. cc: <@712863455467667526>"


def valid_address(address):
    if re.search('^comdex1[0-9a-zA-Z]{38}', address):
        return "comdex"
    elif re.search('^osmo1[0-9a-zA-Z]{38}', address):
        return "osmo"
    elif re.search('^cosmos1[0-9a-zA-Z]{38}', address):
        return "cosmos"
    return False


def get_nonce(chain: str, network: str, guild_id: int):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "nonce/" + str(guild_id) + "_" + str(chain) + "_" + network + ".txt")
    f = open(filename, "r")
    nonce = int(f.readline())
    f.close()
    return nonce


def update_nonce(chain: str, network: str, nonce: int, guild_id: int):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "nonce/" + str(guild_id) + "_" + str(chain) + "_" + network + ".txt")
    f = open(filename, "w")
    f.write(str(nonce + 1))
    f.close()


# Get address balance
def get_address_balance(chain: str, network: str, address: str):
    info = models.get_transaction_details(chain, network)

    amount = 0.0
    try:
        response = json.loads(requests.get(info['balance_url'] + address).text)
        for x in response['balances']:
            if x['denom'] == info['denom']:
                amount = float(x['amount']) / 1000000.00
    except Exception as e:
        print(e)

    return amount


def get_faucet_balance(chain: str, network: str, guild_id: int):
    address = secrets.get_faucet_address(chain, guild_id)
    return get_address_balance(chain, network, address)

# send_testnet_transaction("mainnet", "comdex1zy7uuu6cd5fde3uunlh5l40jjf24ypd6sy9ej4", 1, 837853470136467517)  # mainnet
# send_testnet_transaction("testnet", "comdex1zy7uuu6cd5fde3uunlh5l40jjf24ypd6sy9ej4", 1, 837853470136467517)  # testnet
# send_transaction("osmo", "devnet", "osmo1m8pz6z6gp2twrw4l90mf2mw55sntvrfxt94pl2", 1, 837853470136467517)  # devnet
