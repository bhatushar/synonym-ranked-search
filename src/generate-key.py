import os
from cryptography.fernet import Fernet


os.makedirs("data", exist_ok=True)
with open("data/secret.key", "wb") as key_file:
    key_file.write(Fernet.generate_key())
