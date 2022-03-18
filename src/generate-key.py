import os
from cryptography.fernet import Fernet
from libs import env


os.makedirs(os.path.dirname(env.SECRET_KEY_PATH), exist_ok=True)
with open(env.SECRET_KEY_PATH, "wb") as key_file:
    key_file.write(Fernet.generate_key())
