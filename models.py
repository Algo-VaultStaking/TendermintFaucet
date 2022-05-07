def get_transaction_details(chain: str, network: str):
    if chain == "comdex":
        return {
            "mainnet": {
                'account': 40796,
                'rpc_url': "https://comdex-rpc.polkachu.com",
                "balance_url": "https://rest.comdex.one/cosmos/bank/v1beta1/balances/",
                'chain_id': "comdex-1",
                'denom': "ucmdx"
            },
            "testnet": {
                'account': 126,
                'rpc_url': "https://comets.rpc.comdex.one",
                "balance_url": "https://comets.rest.comdex.one/cosmos/bank/v1beta1/balances/",
                'chain_id': "comets-test",
                'denom': "ucmdx"
            },
            "devnet": {
                'account': 41584,
                'rpc_url': "https://test-rpc.comdex.one",
                "balance_url": "https://test-rest.comdex.one/cosmos/bank/v1beta1/balances/",
                'chain_id': "test-1",
                'denom': "ucmdx"
            }

        }.get(network, {})

    elif chain == "osmo":
        return {
            "mainnet": {
                'rpc_url': "",
                "balance_url": "https://rest.osmosis.zone/cosmos/bank/v1beta1/balances/",
                'chain_id': "",
                'denom': "uosmo"
            },
            "testnet": {
                'rpc_url': "https://testnet-rpc.osmosis.zone",
                "balance_url": "https://testnet-rest.osmosis.zone/cosmos/bank/v1beta1/balances/",
                'chain_id': "osmo-test-4",
                'denom': "uosmo"
            },
            "devnet": {
                'rpc_url': "https://testnet-rpc.osmosis.zone",
                "balance_url": "https://testnet-rest.osmosis.zone/cosmos/bank/v1beta1/balances/",
                'chain_id': "osmo-test-4",
                'denom': "uosmo"
            }

        }.get(network, {})


def get_faucet_account_num(chain: str, network: str, guild_id: int):
    return {
        "comdex": {
            'mainnet': {
                837853470136467517: 0,
                890929797318967416: 40796
            },
            'testnet': {
                837853470136467517: 0,
                890929797318967416: 126
            },
            'devnet': {
                837853470136467517: 58997,
                890929797318967416: 41584
            }
        },
        "osmo": {
            'mainnet': {
                837853470136467517: 0,
                890929797318967416: 0
            },
            'testnet': {
                837853470136467517: 251540,
                890929797318967416: 251372
            },
            'devnet': {
                837853470136467517: 251540,
                890929797318967416: 251372
            }
        }
    }.get(chain, {}).get(network, {}).get(guild_id, 0)