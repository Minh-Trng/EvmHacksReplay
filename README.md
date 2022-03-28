# Replaying hacks on EVM-compatible chains

This project is a python implementation of the hacks covered
in [CMichels repository](https://github.com/MrToph/replaying-ethereum-hacks).

Originally, I planned to extend this repository by many other hacks
that happened on EVM-compatible chains. However, I found the python
tooling for solidity development kinda lacking and decided to move to either 
Javascript/Typescript (Hardhat) or Rust (Foundry) for the purpose of replaying
hacks. Some reasons:
- as of march 2022 brownie does not seem to be well maintained with the last
commit being over a month old. I also had some issues, e.g. [#1482](https://github.com/eth-brownie/brownie/issues/1482)
- hardhat logging (with console.sol) does not work out of the box when integrating
brownie and there are no alternatives that I know of, except for writing view-functions
into the contract whenever something needs to be tested
- the python-solidity community is smaller and the documentation for the tooling seems worse, 
likely making troubleshooting more difficult (haven't had adequate experience with Javascript
yet to evaluate this properly)
- brownie has hardcoded lower bound for solidity compiler (must be >4.22), cant replay hacks
that use contracts with code of older versions (e.g. Parity hack)


# Installation
> pip install -r requirements.txt

> npm install

A valid URL to an archive node has to be provided in tests/config.yml

# Running the tests
Example:
> brownie test tests/test_rari_fuse.py