from cryptography.fernet import Fernet


with open("data/secret.key", "wb") as key_file:
    key_file.write(Fernet.generate_key())
