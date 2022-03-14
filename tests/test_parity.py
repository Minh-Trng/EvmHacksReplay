import pytest
from brownie import network, accounts
from brownie._config import CONFIG
import os
import yaml


@pytest.fixture()
def setup_eth_fork(request):
    fork_blocknumber = request.node.get_closest_marker('brownie_network_name')

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

    yield

    network.disconnect(kill_rpc=True)

@pytest.mark.fork_blocknumber(4501735)
def test_hack(setup_fork):
    raise NotImplementedError