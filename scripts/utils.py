from brownie import network, accounts, config, MockV3Aggregator
from enum import Enum

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_NETWORKS = ["mainnet-fork", "mainnet-fork-dev"]


class Args(Enum):
    DECIMALS = 8
    STARTING_PRICE = 2e8


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_NETWORKS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print("Deploying mocks...")
    print(f"Active network is {network.show_active()}")
    # MockV3Aggregator is the list of all MockV3Aggregator instances
    # If 0 we ned to deploy the mock
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            Args.DECIMALS.value,
            Args.STARTING_PRICE.value,
            {"from": get_account()},
        )
    print("Mocks deployed.")
    price_feed_address = MockV3Aggregator[-1].address
