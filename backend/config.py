
# config.py
import os

class Config:
    GANACHE_URL = os.environ.get('GANACHE_URL', 'http://127.0.0.1:8545')
    CONTRACT_ADDRESS = "0x96d540ef4ACbaDD7De8473B3CbA39EA3dac0d6e6"
