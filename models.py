def get_transaction_details(chain: str, network: str):
    if chain == "comdex":
        return {
            "mainnet": {
                'rpc_url': "https://comdex-rpc.polkachu.com",
                "balance_url": "https://rest.comdex.one/cosmos/bank/v1beta1/balances/",
                "sequence_url": "https://rest.comdex.one/auth/accounts/",
                'chain_id': "comdex-1",
                'denom': "ucmdx"
            },
            "testnet": {
                'rpc_url': "https://meteor.rpc.comdex.one",
                "balance_url": "https://meteor.rest.comdex.one/cosmos/bank/v1beta1/balances/",
                "sequence_url": "https://meteor.rest.comdex.one/auth/accounts/",
                'chain_id': "meteor-test",
                'denom': "ucmdx"
            },
            "devnet": {
                'rpc_url': "https://test-rpc.comdex.one",
                "balance_url": "https://test-rest.comdex.one/cosmos/bank/v1beta1/balances/",
                "sequence_url": "https://test-rest.comdex.one/auth/accounts/",
                'chain_id': "test-1",
                'denom': "ucmdx"
            }

        }.get(network, {})

    elif chain == "osmo":
        return {
            "mainnet": {
                'rpc_url': "",
                "balance_url": "https://rest.osmosis.zone/cosmos/bank/v1beta1/balances/",
                "sequence_url": "https://testnet-rest.osmosis.zone/auth/accounts/",
                'chain_id': "id",
                'denom': "uosmo"
            },
            "testnet": {
                'rpc_url': "https://testnet-rpc.osmosis.zone",
                "balance_url": "https://testnet-rest.osmosis.zone/cosmos/bank/v1beta1/balances/",
                "sequence_url": "https://testnet-rest.osmosis.zone/auth/accounts/",
                'chain_id': "osmo-test-4",
                'denom': "uosmo"
            },
            "devnet": {
                'rpc_url': "https://testnet-rpc.osmosis.zone",
                "balance_url": "https://testnet-rest.osmosis.zone/cosmos/bank/v1beta1/balances/",
                "sequence_url": "https://testnet-rest.osmosis.zone/auth/accounts/",
                'chain_id': "osmo-test-4",
                'denom': "uosmo"
            }

        }.get(network, {})

    elif chain == "cosmos":
        return {
            "mainnet": {
                'rpc_url': "",
                "balance_url": "",
                'chain_id': "",
                'denom': "uosmo"
            },
            "testnet": {
                'rpc_url': "https://rpc.sentry-02.theta-testnet.polypore.xyz",
                "balance_url": "https://rest.sentry-01.theta-testnet.polypore.xyz/cosmos/bank/v1beta1/balances/",
                "sequence_url": "https://rest.sentry-01.theta-testnet.polypore.xyz/auth/accounts/",
                'chain_id': "theta-testnet-001",
                'denom': "uatom"
            },
            "devnet": {
                'rpc_url': "",
                "balance_url": "",
                'chain_id': "",
                'denom': ""
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
                837853470136467517: 132,
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
        },
        "cosmos": {
            'mainnet': {
                837853470136467517: 0,
                890929797318967416: 0
            },
            'testnet': {
                837853470136467517: 697774,
                890929797318967416: 697328
            },
            'devnet': {
                837853470136467517: 0,
                890929797318967416: 0
            }
        }
    }.get(chain, {}).get(network, {}).get(guild_id, 0)
