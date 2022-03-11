import os
from libs import startup


if __name__ == "__main__":
    os.makedirs("data/docs", exist_ok=True)
    os.makedirs("data/encrypted", exist_ok=True)
    os.makedirs("data/meta", exist_ok=True)

    print("Computing metadata: TF and IFD")
    startup.compute_metadata()
    print("Encrypting documents")
    startup.encrypt_docs()
