import os

import pytest
import yaml
from brownie import network
from brownie._config import CONFIG
import brownie.project as project

@pytest.fixture(scope='session')
def brownie_project():
    project.load('.')
    return project.EvmhacksreplayProject

@pytest.fixture()
def eth_fork_network(request):
    # brownie automatically starts ganache for some reason
    network.disconnect(kill_rpc=True)

    fork_blocknumber = request.node.get_closest_marker('fork_blocknumber').args[0]

    file_dir = os.path.dirname(__file__)

    with open(f'{file_dir}/config.yml', 'r') as f:
        config = yaml.safe_load(f)

    rpc_url = config["ETHEREUM_RPC_URL"]
    brownie_id = "fork-at-block"

    network_config = {
        "name": "Ganache-CLI (Mainnet Fork)",
        "id": brownie_id,
        "cmd": "ganache-cli",
        "host": "http://127.0.0.1",
        "timeout": 120,
        "cmd_settings": {
            "port": 8545,
            "gas_limit": 12000000,
            "accounts": 10,
            "evm_version": "istanbul",
            "mnemonic": "brownie",
            "fork": f"{rpc_url}@{fork_blocknumber}"
        }
    }

    CONFIG.networks[brownie_id] = network_config

    network.connect(brownie_id)

    yield network

    network.disconnect(kill_rpc=True)