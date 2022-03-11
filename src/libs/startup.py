import os
from cryptography.fernet import Fernet
from libs import preprocessing, tf_idf


# Calculate term frequencies and inverse document frequencies
def compute_metadata():
    """
    Generate Term Frequency and Inverse Document Frequency for documents in "data/docs".
    The term frequencies for "file.txt" is stored in "data/meta/file.txt.csv".
    The inverse document frequencies are stored in "data/meta/_idf.csv".
    The records are stored in the ascending order of the keywords.
    """

    ref_count: dict[str, int] = dict()  # Count how many documents contain a term

    for doc in os.listdir("data/docs"):
        with open(f"data/docs/{doc}", "r", encoding="utf-8") as file:
            text = file.read()
        words = preprocessing.sanitize_text(text)
        df = tf_idf.term_frequency(words)
        df.to_csv(f"data/meta/{doc}.csv")

        # Record document references
        for term in df["Terms"]:
            ref_count[term] = ref_count.get(term, 0) + 1

    df = tf_idf.inverse_document_frequency(ref_count)
    df.to_csv("data/meta/_idf.csv")


def encrypt_docs():
    """
    Encrypt all documets in "data/docs/" using `Fernet` cipher and "data/secret.key".
    The encrypted documents are stored in "data/encrypted/".
    """

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
