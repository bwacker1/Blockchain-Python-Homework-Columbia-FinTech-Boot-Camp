# Blockchain-Python-Homework-Columbia-FinTech-Boot-Camp

## Overview

This project allows a user to derive testnet BitCoin and Ethereum crypto wallets from a cryptocurrency account, and send transactions between wallets via Python in a command line interface. 

## Dependencies

In order to run, you must ensure that:
* The [hd-wallet-derive](https://github.com/dan-da/hd-wallet-derive) repo is added into the "wallet" directory. It was not possible to push the repo to GitHub with this included in it.  
* The following libraries and technologies are installed in your developer environment:
  * Web3
  * Bit
  * PHP
  * [MyCrypto](https://mycrypto.com/)

## Instructions

1. Execute the **mnemonic.sh** file
2. Direct to the **wallet** directory in your Command Prompt / Terminal.
3. Run `python`
4. Within the Python shell, run the command `from wallet import *`
5. Derive the crypto wallets associated with the account using the following function:
    * `derive_wallets(mnemonic,{BTCTEST or ETH},{# of wallets to derive})`

### BitCoin

6. Ensure the account you would like to send funds from has been topped up via a [testnet faucet](https://coinfaucet.eu/en/btc-testnet/).
    * Use the **address** output from the desired account.
7. Initiate a transaction using the following function:
    * `send_tx(BTCTEST,{sender address from step 6},{receiving address},{amount})`
8. Monitor the transaction on a [block explorer](https://tbtc.bitaps.com/). 

### Ethereum

6. Add one of the ETH addresses to the pre-allocated accounts in your **networkname.json** file.
7. Delete the geth folder in each node, then re-initialize using `geth --datadir nodeX init networkname.json`. This will create a new chain, and will pre-fund the new account.
8. Due to a bug in **web3.py**, you will need to send a transaction or two with MyCrypto first, since the `w3.eth.generateGasPrice()` function does not work with an empty chain. You can use one of the ETH address privkey, or one of the node keystore files.
9. Initiate a transaction using the following function:
    * `send_tx(ETH,{sender address from step 6},{receiving address},{amount})`
10. Monitor the transaction on MyCrypto by inputting the `txid` into the TX Status section.
