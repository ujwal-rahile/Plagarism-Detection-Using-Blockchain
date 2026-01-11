
# app/__init__.py
from flask import Flask
from flask_cors import CORS
from .api import api_bp

def create_app():
    app = Flask(__name__)
    CORS(app) # Enable CORS for frontend communication
    
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
