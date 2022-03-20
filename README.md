# Synonym based ranked search over encrypted data

This project is a proof of concept for implementing ranked search over encrypted data in a cloud environment with support for synonyms in the query.

It is done in partial fulfilment of the Cloud Computing Principles course at NIT Trichy.

## Folder structure

```
root
 |- data
 |   |- docs (Contains text documents of user data)
 |   |- digests (MD5 hashes of user documents)
 |   |- encrypted (Encrypted form of documents)
 |   |- meta (Contains CSV files for TF and IDF)
 |- src (Executable scripts)
 |   |- libs (Importable libraries)
```

## How it works

### Preprocessing

Word tokens are extracted from each document and unhelpful words are removed from the collection. This includes stopwords, single character words, and punctualtions.

The filtered words are lemmatized which replaces similar meaning words with a common synonym. Finally, the words are also stemmed which reduces a word to its root (e.g. "playing" and "played" are reduced to "play"). Difference between lemmatizing and stemming is that the output of lemmatizing is a part of the vocabulary.

### TF-IDF

Term Frequency: Measures the frequency of a word in a document.
<br>
Inverse Document Frequency: Measures the informativeness of a term with respect to all documents.

```
N = Total number of distinct keywords in dataset
F(d,w) = Number of times keyword w appeares in docment d
D(w) = Number of documents containing the keyword w
TF(d, w) = 1 + ln(F(d, w))
IDF(w) = ln(1 + N / D(w))
```

### Encrypting document

The documents are encrypted using Fernet's cipher. The cryptography key is stored in `data/secret.key`. This is also used to decrypt the search results. In a real-world application, the documents are encrypted/decrypted on the client machine before being uploaded to the cloud along with the metadata.

### Search

This project employees a TF-IDF based ranked searching algorithm. The similarity of a document to a query is computed by the rank function:

<!-- $$
\text{Rank}(Q, d) = \frac{\sum_{w \in Q} TF(d, w) \times IDF(w)}{\sqrt{\sum_{w \in Q} (TF{d, w})^2} \times \sqrt{\sum_{w \in Q} (IDF(w))^2}}
$$ -->

<div align="center"><img style="background: white;" src="svg\uKBA5fP57x.svg"></div>

A lower rank value means a higher similarity. For a search query, all documents are returned along with their matching score in the order of relevance.

Before starting the search, the query is passed through the same preprocessing as the text documents. This maps query terms to the ones stored in the metadata and provides limited synonym support in search queries.

### Caching

Metadata computation is a resource intensive task. Therefore, the term frequencies and ciphertext of the documents are preserved between execution.

An MD5 hash is generated for each document. If the hash doesn't match with the pre-existing hash, metadata and ciphertext is re-calculated. If a document is deleted between execution, then the corresponding files are also deleted upon program startup.

The IDF is always re-calculated. While it can be optimized, it's not as demanding a task as computing TF for each document.

## Installation

The project is written in Python 3.10.2. Before proceeding, create and activate a virtual environment.

Download text document dataset into `data/docs`.

Install the dependencies:

```
pip install -r requirements.txt
```

Download NLTK data inside `venv/nltk_data`:

```
python src/nltk-download.py
```

Generate the encryption/decryption key:

```
python src/generate-key.py
```

Start the application:

```
python src/main.py
```

## Usage

After metadata computation has finished, the user can enter their search query. Longer queries tend to produce more accurate research but take longer to be processed.

Once the search results are returned, a file can be decrypted an opened by it's index. Enter `q` to return to query input.

## Testing

Generate queries by extracting lines from documents. Output is a CSV file with two columns: Files, Queries.

```
python src/generate-query.py
```

Run search on the generated queries to find the average search time and the mean squared error using the search result ranks.

```
python src/run-tests.py
```

## References

Research Paper: [Achieving effective cloud search services: multi-keyword ranked search over encrypted cloud data supporting synonym query](https://ieeexplore.ieee.org/document/6780939)

Dataset: [Books in plaintext for training language models](https://www.kaggle.com/paulrohan2020/huge-books-in-plain-text-for-train-language-models)
