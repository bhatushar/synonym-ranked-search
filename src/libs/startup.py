import os
from cryptography.fernet import Fernet


def encrypt_docs():
    # Initialize cipher with secret key
    with open("data/secret.key", "rb") as key_file:
        cipher = Fernet(key_file.read())

    # Encrypt all files in data/docs/ while keeping the original name
    for doc in os.listdir("data/docs"):
        doc_file = open(f"data/docs/{doc}", "rb")
        ciphertext = cipher.encrypt(doc_file.read())
        enc_file = open(f"data/encrypted/{doc}", "wb")
        enc_file.write(ciphertext)
        doc_file.close()
        enc_file.close()
