
# config.py
import os

class Config:
    GANACHE_URL = os.environ.get('GANACHE_URL', 'http://127.0.0.1:8545')
    CONTRACT_ADDRESS = "0xFEdA61D0CD0b151389f312c297EaE239154ab92D"
    # ABI Should ideally be loaded from a file or environment, but for now we keep it here as per user's state
    # I'll put the ABI in a separate constant file or service to keep config clean, 
    # but for simplicity in this step, I'll pass it to the service constructor.
