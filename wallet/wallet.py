# importing libraries
from constants import *
import os
from dotenv import load_dotenv
import subprocess
import json
from eth_account import Account
from bit import PrivateKeyTestnet
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
from bit.network import NetworkAPI

load_dotenv()

# calling mnemonic environment variable
mnemonic = os.getenv('MNEMONIC')

# function to derive wallets
def derive_wallets (mnemonic, coin, number):
    
    command = f"./derive -g --mnemonic='{mnemonic}' --coin='{coin}' --numderive='{number}' --cols=address,index,path,address,privkey,pubkey,pubkeyhash,xprv,xpub --format=json"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = process.communicate()
    process_status = process.wait()
    keys = json.loads(output)
    
    return keys

# function to call derive_wallets function for BTCTEST and ETH currencies and output a dictionary
# with derived information for three accounts per coin
def coins ():

    coin_dict = {
        'btc-test' : derive_wallets(mnemonic, BTCTEST, 3),
        'eth' : derive_wallets(mnemonic, ETH, 3)
    }
    
    return coin_dict

# function to convert private key into a readable format for web3 / bit
def priv_key_to_account (coin, priv_key):
    
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

# setting sender ETH account
eth_account = priv_key_to_account(ETH,coins()[ETH][0]['privkey'])

# setting a receiver ETH address
eth_address = coins()[ETH][1]['address']

# setting sender BTCTEST account
btctest_account = priv_key_to_account(BTCTEST,coins()[BTCTEST][0]['privkey'])

# setting a receiver BTCTEST address
btctest_address = coins()[BTCTEST][1]['address']

# setting up Web3 port
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# function to create raw, unsigned transaction
def create_tx(coin, account, to, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas({
            "from": account.address, 
            "to": to, 
            "value": w3.toWei(amount,'ether') 
        })
        return {
            "from": account.address,
            "to": to,
            "value": w3.toWei(amount,'ether') ,
            "gas": gasEstimate,
            "gasPrice": w3.eth.gasPrice,
            "nonce": w3.eth.getTransactionCount(account.address),
            #"chainID": w3.net.chainId --this has been deprecated
        }
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
    
# function to create, sign, and send transaction 
def send_tx(coin, account, recipient, amount):
    
    raw_tx = create_tx(coin, account, recipient, amount)
    signed_tx = account.sign_transaction(raw_tx)
    
    if coin == ETH:
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return result
    elif coin == BTCTEST:
        return NetworkAPI.broadcast_tx_testnet(signed_tx)

# sending ETH transaction
send_tx(ETH,eth_account,eth_address,1)

# sending BTCTEST transaction
send_tx(BTCTEST,btctest_account,btctest_address,0.001)