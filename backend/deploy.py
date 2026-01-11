import json
import os
from web3 import Web3

GANACHE_URL = os.getenv("GANACHE_URL", "http://ganache:8545")
web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

def deploy():
    if not web3.is_connected():
        print("Failed to connect to Ganache")
        return

    # Get the first account
    accounts = web3.eth.accounts
    sender = accounts[0]
    print(f"Deploying from account: {sender}")

    # Load ABI and Bytecode
    # Note: build is in /app/build in the container
    with open("build/PlagiarismChecker.abi", "r") as f:
        abi = json.load(f)
    
    with open("build/PlagiarismChecker.bin", "r") as f:
        bytecode = f.read().strip()

    # Update app/abi.json for the backend service to use
    with open("app/abi.json", "w") as f:
        json.dump(abi, f, indent=4)
    print("Updated app/abi.json")
    
    # Deploy
    Contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = Contract.constructor().transact({'from': sender})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Contract deployed at: {tx_receipt.contractAddress}")
    
    # Update config.py
    with open("config.py", "r") as f:
        lines = f.readlines()
    
    with open("config.py", "w") as f:
        for line in lines:
            if "CONTRACT_ADDRESS" in line:
                f.write(f'CONTRACT_ADDRESS = "{tx_receipt.contractAddress}"\n')
            else:
                f.write(line)
    print("Updated config.py with new address")

if __name__ == "__main__":
    deploy()
