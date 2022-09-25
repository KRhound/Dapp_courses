from audioop import add
from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()
install_solc("0.8.7")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


# compile Our Solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.7",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/33310c684af2401c8a2255245be7d9e4")
)
chain_id = 4
my_address = "0xd33b2ACaA8cac4435c31A23E91e7aDA3ec393FDc"
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latestest transaction
nonce = w3.eth.getTransactionCount(my_address)
# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# Send this signed transation
print("Deploying Contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")
# Working with the contract, you always need
# Contract Address
# Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making the call and getting a return value
# Transact -> Actually make a state change

# Initial value of favorite number
print(simple_storage.functions.retrieve().call())
print("Updating Contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!")
print(simple_storage.functions.retrieve().call())
