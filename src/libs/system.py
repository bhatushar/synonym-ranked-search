import os
import shutil
import webbrowser
from cryptography.fernet import Fernet
from libs import env, preprocessing, tf_idf


def mkdirs():
    """
    Create directories that are needed for program execution
    """

    os.makedirs(env.DOCS_PATH, exist_ok=True)
    os.makedirs(env.ENC_DOCS_PATH, exist_ok=True)
    os.makedirs(env.METADATATA_PATH, exist_ok=True)


def compute_metadata():
    """
    Generate Term Frequency and Inverse Document Frequency for documents in "data/docs".
    The term frequencies for "file.txt" is stored in "data/meta/file.txt.csv".
    The inverse document frequencies are stored in "data/meta/_idf.csv".
    The records are stored in the ascending order of the keywords.
    """

    ref_count: dict[str, int] = dict()  # Count how many documents contain a term

    for doc in os.listdir(env.DOCS_PATH):
        with open(f"{env.DOCS_PATH}/{doc}", "r", encoding="utf-8") as file:
            text = file.read()
        words = preprocessing.sanitize_text(text)
        df = tf_idf.term_frequency(words)
        df.to_csv(f"{env.METADATATA_PATH}/{doc}.csv")

        # Record document references
        for term in df["Terms"]:
            ref_count[term] = ref_count.get(term, 0) + 1

    df = tf_idf.inverse_document_frequency(ref_count)
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
    for doc in os.listdir(env.DOCS_PATH):
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


def cleanup():
    """
    Remove data generated by the program.
    This includes decrypted, encrypted, and metadata files.
    """

    if os.path.exists(env.DEC_DOC_PATH):
        os.remove(env.DEC_DOC_PATH)
    shutil.rmtree(env.ENC_DOCS_PATH)
    shutil.rmtree(env.METADATATA_PATH)