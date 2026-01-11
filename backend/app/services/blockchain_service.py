
from web3 import Web3
import json
import os
from ..utils.text_processing import extract_text_chunks
from config import Config

class BlockchainService:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(Config.GANACHE_URL))
        self.contract_address = Config.CONTRACT_ADDRESS
        
        # Load ABI from file
        abi_path = os.path.join(os.path.dirname(__file__), '..', 'abi.json')
        with open(abi_path, 'r') as f:
            self.abi = json.load(f)

        self.contract = self.web3.eth.contract(address=Web3.to_checksum_address(self.contract_address), abi=self.abi)

    def is_connected(self):
        return self.web3.is_connected()

    def get_balance(self, address):
        balance = self.web3.eth.get_balance(address)
        return float(self.web3.from_wei(balance, 'ether'))

    def validate_account(self, address):
        return address in self.web3.eth.accounts

    def process_document(self, filename, sender_address):
        """
        Processes a document: extracts, hashes, and validates against blockchain.
        """
        hashes, segments = extract_text_chunks(filename)
        if not hashes:
            return {"error": "No text content found"}
        
        # Ensure 0x prefix
        formatted_hashes = ['0x' + h if not h.startswith('0x') else h for h in hashes]
        
        try:
            initial_balance = self.get_balance(sender_address)
            
            tx_hash = self.contract.functions.checkAndStoreHashes(formatted_hashes).transact({'from': sender_address})
            receipt = self.web3.eth.get_transaction_receipt(tx_hash)
            
            result = {
                "initial_balance": initial_balance,
                "final_balance": self.get_balance(sender_address),
                "is_valid": False,
                "plagiarism_percent": 0,
                "plagiarized_content": []
            }

            # Parse Event
            logs = self.contract.events.PlagiarismDetected().process_receipt(receipt)
            # Logic: If event emitted, it contains the details. 
            if logs:
                event_args = logs[0]['args']
                result["plagiarism_percent"] = event_args['similarityPercentage']
                indices = event_args['plagiarizedIndices']
                
                # Map indices to content
                result["plagiarized_content"] = [segments[i] for i in indices if i < len(segments)]
                result["is_valid"] = result["plagiarism_percent"] < 20
            
            return result
            
        except Exception as e:
            return {"error": str(e)}

