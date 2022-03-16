import pytest
from brownie import accounts

from setup_fixtures import brownie_project, eth_fork_network

#https://cmichel.io/replaying-ethereum-hacks-sushiswap-badger-dao-digg/

@pytest.mark.fork_blocknumber(11940499)
def test_hack(eth_fork_network, brownie_project):
    sushi_factory = brownie_project.interface.IUniswapV2Factory('0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac')
    sushi_maker = brownie_project.interface.ISushiMaker('0xe11fc0b43ab98eb91e9836129d1ee7c3bc95df50')

    weth = brownie_project.interface.IWETH('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')

    digg_wbtc_pair = brownie_project.interface.IUniswapV2Pair('0x9a13867048e01c663ce8Ce2fE0cDAE69Ff9F35E3')

    attacker_eoa = accounts[0]
    sushi_router_addr = '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F'
    attacker_contract = brownie_project.BadgerDaoAttacker.deploy(
        sushi_router_addr,
        sushi_factory.address,
        {'from': attacker_eoa})

    assert True