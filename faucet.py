import re
import os
import secrets
from logger import log
from tendermintwallet import Transaction
import requests
import json


# Send a transaction to the requestor
def send_transaction(chain: str, network: str, address: str, tokens: float, guild_id: int):
    nonce = get_nonce(chain, network, guild_id)
    tokens = int(tokens * 1000000)

    info = get_transaction_details(chain, network)

    tx = Transaction(
        privkey=bytes.fromhex(secrets.get_faucet_key(guild_id)),
        account_num=info['account'],
        sequence=nonce,
        fee=5000,
        gas=80000,
        fee_denom=info['denom'],
        memo="",
        chain_id=info['chain_id'],
        sync_mode="broadcast_tx_sync",
    )

    tx.add_transfer(recipient=address, amount=tokens, denom=info['denom'])
    pushable_tx = tx.get_pushable()
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }

    response = requests.post(info['url'], data=pushable_tx, headers=headers, verify=False)
    print(response.text)
    response = json.loads(response.text)

    try:
        if response['result']['code'] == 0:
            log("Sent testnet transaction to " + address)
            update_nonce(chain, network, nonce, guild_id)
            return response['result']['hash']
        else:
            log("Failed to send to " + address)
            return False
    except:
        log("Failed to send to " + address)
        return False


def get_transaction_details(chain: str, network: str):
    if chain == "comdex":
        denom = "ucmdx"
        if network == "mainnet":
            account = 40796
            url = 'https://comdex-rpc.polkachu.com'
            chain_id = "comdex-1"

        elif network == "testnet":
            account = 126
            url = "https://comets.rpc.comdex.one"
            chain_id = "comets-test"

        elif network == "devnet":
            account = 41584
            url = 'https://test-rpc.comdex.one'
            chain_id = "test-1"
        else:
            return False

    elif chain == "osmosis":
        denom = "uosmo"
        if network == "mainnet":
            account = 0
            url = ''
            chain_id = ""

        elif network == "testnet":
            account = 251372
            url = " https://testnet-rpc.osmosis.zone"
            chain_id = "osmo-test-4"

        elif network == "devnet":
            account = 251372
            url = ' https://testnet-rpc.osmosis.zone'
            chain_id = "osmo-test-4"
        else:
            return False
    else:
        return False
    return {"account": account, "url": url, "chain_id": chain_id, "denom": denom}


def valid_address(address):
    if re.search('^comdex1[0-9a-zA-Z]{38}', address):
        return "comdex"
    elif re.search('^osmo1[0-9a-zA-Z]{38}', address):
        return "osmosis"
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
    if chain == "comdex":
        if network == "mainnet":
            url = "https://rest.comdex.one/cosmos/bank/v1beta1/balances/" + address

        elif network == "testnet":
            url = "https://comets.rest.comdex.one/cosmos/bank/v1beta1/balances/" + address

        elif network == "devnet":
            url = "https://test-rest.comdex.one/cosmos/bank/v1beta1/balances/" + address
        else:
            # default to devnet
            url = "https://test-rest.comdex.one/cosmos/bank/v1beta1/balances/" + address

    elif chain == "osmosis":
        if network == "mainnet":
            url = "https://rest.osmosis.zone/cosmos/bank/v1beta1/balances/" + address

        elif network == "testnet":
            url = "https://testnet-rest.osmosis.zone/cosmos/bank/v1beta1/balances/" + address

        elif network == "devnet":
            url = "https://testnet-rest.osmosis.zone/cosmos/bank/v1beta1/balances/" + address
        else:
            # default to devnet
            url = "https://testnet-rest.osmosis.zone/cosmos/bank/v1beta1/balances/" + address

    amount = 0.0
    try:
        response = json.loads(requests.get(url).text)
        for x in response['balances']:
            if x['denom'] == "ucmdx" or x['denom'] == "uosmo":
                amount = float(x['amount']) / 1000000.00
    except Exception as e:
        print(e)

    return amount


def get_faucet_balance(chain: str, network: str, guild_id: int):
    address = secrets.get_faucet_address(chain, guild_id)
    return get_address_balance(chain, network, address)


# send_testnet_transaction("mainnet", "comdex1zy7uuu6cd5fde3uunlh5l40jjf24ypd6sy9ej4", 1, 890929797318967416)  # mainnet
# send_testnet_transaction("testnet", "comdex1zy7uuu6cd5fde3uunlh5l40jjf24ypd6sy9ej4", 1, 890929797318967416)  # testnet
# send_testnet_transaction("devnet", "comdex1x7xkvflswrxnkwd42t55jxl9hkhtnnlt43dqs3", 0.5, 890929797318967416)  # devnet
