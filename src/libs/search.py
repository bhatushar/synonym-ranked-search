import os
import numpy as np
import pandas as pd
from libs import preprocessing


def query_idf(query_terms: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Find IDF of terms in the sanitized query.

    Parameter
    ---------
        query_term: numpy.ndarray[str]
            Sanitized terms extracted from original query

    Returns
    -------
        tuple[numpy.ndarray[str], numpy.ndarray[float]]
            First element is an array of sorted terms for which IDF exists.
            Second element is an array of IDF.
    """

    idf_df = pd.read_csv("data/meta/_idf.csv")
    rows = idf_df.loc[
        idf_df["Terms"].isin(query_terms)
    ]  # Rows of DF which contain query terms
    existing_terms = rows["Terms"].to_numpy()
    idf = rows["IDF"].to_numpy()
    return existing_terms, idf


def query_tf(query_terms: np.ndarray, csv_path: str) -> np.ndarray:
    """
    Find TF of query terms in given CSV file.

    Parameters
    ----------
        query_terms: numpy.ndarray[str]
            Sanitized terms extracted from original query.
            Array should be sorted and the terms should exist in _idf.csv.
        csv_path: str
            Path to CSV file containing term frequencies

    Returns
    -------
        numpy.ndarray[float]
            Term frequencies in the order of query_terms.
            If term doesn't exist in document, TF is 0.
    """

    tf_df = pd.read_csv(csv_path)
    tf = np.full((query_terms.size), 0)
    rows = tf_df.loc[
        tf_df["Terms"].isin(query_terms)
    ]  # Rows of DF which contain query terms
    for index, term in enumerate(query_terms):
        row = rows.loc[
            rows["Terms"] == term
        ]  # INEFFICIENT: query_terms and rows["Terms"] are sorted
        if len(row) > 0:
            tf[index] = row.iloc[0]["TF"]
    return tf


def find_docs(query: str) -> list[tuple[str, float]]:
    """
    Performs TFxIDF based search and returns matching documents in ranked order.

    The similarity score is computed as follows:
    ```
    Q: Query terms
    IDF(Q): Array of inverse document frequencies of query terms
    TF(Q, d): Array of query term frequencies in document d
    Score(Q, d): Similarity score of Q and d. Lower score means d is more relevant to Q.
    Weight(array) = sqrt(sum(array ** 2))
    Score(Q, d) = sum(TF * IDF) / [Weight(IDF(Q)) * Weight(TF(Q, d))]
    ```

    Parameter
    ---------
        query: str

    Returns
    -------
        list[tuple[str, float]]
            Pairs of document name and their similarity score.
            Documents are ordered from most to least relevant.
    """
    query_terms = preprocessing.sanitize_text(query)

    query_terms, idf = query_idf(query_terms)
    idf_weight: float = np.sqrt(np.square(idf).sum())  # sqrt(sum(idf ^ 2))

    scores: list[(str, float)] = []
    meta_docs = [
        doc for doc in os.listdir("data/meta") if doc != "_idf.csv"
    ]  # Ignore IDF file
    for doc in meta_docs:
        tf = query_tf(query_terms, f"data/meta/{doc}")
        # Compute similarity score
        tf_weight: float = np.sqrt(np.square(tf).sum())  # sqrt(sum(tf ^ 2))
        tf_idf_sum: float = np.multiply(tf, idf).sum()  # sum(tf * idf)
        tf_idf_weight = np.multiply(tf_weight, idf_weight)
        # Store score
        if tf_idf_weight == 0:
            scores.append((doc[:-4], 0))
        else:
            scores.append((doc[:-4], np.divide(tf_idf_sum, tf_idf_weight)))

    scores = sorted(scores, key=lambda s: s[1])
    return scores
