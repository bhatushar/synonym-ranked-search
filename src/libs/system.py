import hashlib
import os
import shutil
import webbrowser
from cryptography.fernet import Fernet
from libs import env, preprocessing, tf_idf


changed_files: list[str] = []
"""
List of documents that are added or modified since last execution
"""


def mkdirs():
    """
    Create directories that are needed for program execution
    """

    os.makedirs(env.DOCS_PATH, exist_ok=True)
    os.makedirs(env.DIGESTS_PATH, exist_ok=True)
    os.makedirs(env.ENC_DOCS_PATH, exist_ok=True)
    os.makedirs(env.METADATATA_PATH, exist_ok=True)


def cleanup_deleted():
    """
    If any document is deleted, remove files associated with it.
    These files includes hash digests, encrypted text and term frequencies.
    """
    docs = set(os.listdir(env.DOCS_PATH))
    # Files which don't exist in "data/docs" but has a digest
    deleted_files = [file for file in os.listdir(env.DIGESTS_PATH) if file not in docs]
    # Delete digest, encrypted, and metadata
    for file in deleted_files:
        os.remove(f"{env.DIGESTS_PATH}/{file}")
        os.remove(f"{env.ENC_DOCS_PATH}/{file}")
        os.remove(f"{env.METADATATA_PATH}/{file}.csv")


def check_changes():
    """
    Uses MD5 hash to check if any of the files are changed
    """
    changed_files.clear()

    for doc in os.listdir(env.DOCS_PATH):
        with open(f"{env.DOCS_PATH}/{doc}", "rb") as file:
            digest = hashlib.md5(file.read()).hexdigest()
        if not os.path.exists(f"{env.DIGESTS_PATH}/{doc}"):
            # Digest doesn't exist, new file
            changed_files.append(doc)
            with open(f"{env.DIGESTS_PATH}/{doc}", "w") as file:
                file.write(digest)
        else:
            # Compare with old digest
            with open(f"{env.DIGESTS_PATH}/{doc}", "r+") as file:
                org_digest = file.read()
                if org_digest != digest:
                    # Different digests, modified file
                    changed_files.append(doc)
                    file.truncate(0)
                    file.write(digest)


def compute_metadata():
    """
    Generate Term Frequency and Inverse Document Frequency for documents in "data/docs".
    The term frequencies for "file.txt" is stored in "data/meta/file.txt.csv".
    The inverse document frequencies are stored in "data/meta/_idf.csv".
    The records are stored in the ascending order of the keywords.
    """

    for doc in changed_files:
        # Only compute term frequencies for files which are modified
        with open(f"{env.DOCS_PATH}/{doc}", "r", encoding="utf-8") as file:
            text = file.read()
        words = preprocessing.sanitize_text(text)
        df = tf_idf.term_frequency(words)
        df.to_csv(f"{env.METADATATA_PATH}/{doc}.csv")

    # IDF is always computed because I'm too lazy to optimize it
    df = tf_idf.inverse_document_frequency()
    df.to_csv(env.IDF_CSV_PATH)


def encrypt_docs():
    """
    Encrypt all documets in "data/docs/" using `Fernet` cipher and "data/secret.key".
    The encrypted documents are stored in "data/encrypted/".
    """

    # Initialize cipher with secret key
    with open(env.SECRET_KEY_PATH, "rb") as key_file:
        cipher = Fernet(key_file.read())

    # Encrypt all files in data/docs/ while keeping the original name
    for doc in changed_files:
        doc_file = open(f"{env.DOCS_PATH}/{doc}", "rb")
        ciphertext = cipher.encrypt(doc_file.read())
        enc_file = open(f"{env.ENC_DOCS_PATH}/{doc}", "wb")
        enc_file.write(ciphertext)
        doc_file.close()
        enc_file.close()


def open_doc(doc: str):
    """
    Decrypt file and open it in a text editor

    Parameter
    ---------
        doc: str
            Name of the document to be encrypted
    """

    with open(env.SECRET_KEY_PATH, "rb") as key_file:
        cipher = Fernet(key_file.read())

    doc_file = open(f"{env.ENC_DOCS_PATH}/{doc}", "rb")
    data = cipher.decrypt(doc_file.read())
    out_file = open(env.DEC_DOC_PATH, "wb")
    out_file.write(data)

    doc_file.close()
    out_file.close()

    webbrowser.open(os.path.abspath(env.DEC_DOC_PATH))
