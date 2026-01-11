
from flask import Blueprint, request, jsonify
from eth_account import Account
from ..services.blockchain_service import BlockchainService
import os

api_bp = Blueprint('api', __name__)
blockchain_service = BlockchainService()

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    passkey = data.get('passkey')
    
    if not passkey:
        return jsonify({"error": "Passkey is required"}), 400
        
    try:
        # 1. Validate Format
        try:
            account = Account.from_key(passkey)
            sender_address = account.address
        except Exception:
            return jsonify({"error": "Invalid passkey format"}), 400
            
        # 2. Validate Authorization
        if not blockchain_service.validate_account(sender_address):
             return jsonify({"error": "Account not authorized on this network"}), 401
             
        # 3. Get Balance
        balance = blockchain_service.get_balance(sender_address)
        
        return jsonify({
            "address": sender_address,
            "balance": balance,
            "message": "Login successful"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    sender = request.form.get('sender')
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if not sender:
        return jsonify({"error": "Sender address required"}), 400

    # Save temp file for processing (could be optimized to stream)
    temp_path = f"temp_{file.filename}"
    file.save(temp_path)
    
    try:
        result = blockchain_service.process_document(temp_path, sender)
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        if "error" in result:
             return jsonify(result), 400
             
        return jsonify(result)
        
    except Exception as e:
        # Cleanup on error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({"error": str(e)}), 500
