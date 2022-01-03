from solcx import compile_standard
from solcx import install_solc
import json
from web3 import Web3
import os

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile our solidity
install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "SimpleStorage.sol": {
                "content": simple_storage_file
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"][
    "evm"]["bytecode"]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. Build transaction
# 2. Sign transaction
# 3. Send transaction

transaction = SimpleStorage.constructor().buildTransaction({
    "gasPrice": w3.eth.gas_price,
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce
})

signed_txn = w3.eth.account.sign_transaction(transaction,
                                             private_key=private_key)

# send signed transaction

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Working with the contract
# Contract Address
# Contract ABI

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making the call and getting a return value NO STATE CHANGE
# Transact -> State change

# Initial Value of favorite number
print(simple_storage.functions.retrieve().call())

store_transaction = simple_storage.functions.store(77).buildTransaction({
    "gasPrice":
    w3.eth.gas_price,
    "chainId":
    chain_id,
    "from":
    my_address,
    "nonce":
    nonce + 1
})

signed_store_transaction = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key)
signed_txn_hash = w3.eth.send_raw_transaction(
    signed_store_transaction.rawTransaction)
store_txn_receipt = w3.eth.wait_for_transaction_receipt(signed_txn_hash)
