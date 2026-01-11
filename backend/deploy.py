import json
import os
from web3 import Web3
from solcx import compile_standard, install_solc

# Install specific Solidity version
install_solc("0.8.20")

GANACHE_URL = os.getenv("GANACHE_URL", "http://ganache:8545")
web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

CONTRACT_FILE = "contract/paper.sol"
HASH_FILE = "contract/.contract_hash"

import hashlib

def get_file_hash(filepath):
    """Calculates SHA256 hash of a file."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def check_and_deploy():
    """Checks if contract changed and deploys if needed."""
    if not os.path.exists(CONTRACT_FILE):
        print(f"⚠️ Warning: {CONTRACT_FILE} not found. Skipping auto-deploy check.")
        return

    current_hash = get_file_hash(CONTRACT_FILE)
    stored_hash = None

    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            stored_hash = f.read().strip()

    if current_hash != stored_hash:
        print("📝 Contract change detected (or first run). Deploying...")
        try:
            deploy()
            # Update stored hash only if deployment succeeds
            if current_hash:
                with open(HASH_FILE, "w") as f:
                    f.write(current_hash)
            print("✅ Deployment complete and hash updated.")
        except Exception as e:
            print(f"❌ Deployment failed: {e}")
    else:
        print("⚡ Contract unchanged. Skipping deployment.")


def deploy():
    if not web3.is_connected():
        print("Failed to connect to Ganache")
        return

    # Get the first account
    accounts = web3.eth.accounts
    sender = accounts[0]
    print(f"Deploying from account: {sender}")

    # Compile Solidity
    with open("contract/paper.sol", "r") as f:
        paper_file_content = f.read()

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"Paper.sol": {"content": paper_file_content}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.8.20",
    )

    bytecode = compiled_sol["contracts"]["Paper.sol"]["PlagiarismChecker"]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"]["Paper.sol"]["PlagiarismChecker"]["abi"]

    # Update contract/abi.json for the backend service to use
    with open("contract/abi.json", "w") as f:
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
                # Keep indentation if it exists
                prefix = line[:line.find("CONTRACT_ADDRESS")]
                f.write(f'{prefix}CONTRACT_ADDRESS = "{tx_receipt.contractAddress}"\n')
            else:
                f.write(line)
    print("Updated config.py with new address")

if __name__ == "__main__":
    deploy()
