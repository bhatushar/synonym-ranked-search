import os
import numpy as np
import pandas as pd
from libs import env


def term_frequency(words: np.ndarray) -> pd.DataFrame:
    """
    Compute weighted term frequencies using the words array.

    Word Frequency, `WF(w)`: Number of times word w appeared in `words`

    Word Count, `WC`: Size of `words` array

    `Weighted TF(w) = 1 + ln(WF(w) / WC)`

    Parameters
    ----------
        words: numpy.ndarray[str]
            Array of words extracted from the text

    Returns
    -------
    pandas.DataFrame
        Data frame with 3 columns: `Terms`, `Count`, `TF`.
        `Terms` is the word taken from `words` array.
        `Count` is the number of times a word occurs.
        `TF` is the weighted term frequency.
        Data frame is sorted on `Terms` column.
    """

    terms, frequencies = np.unique(words, return_counts=True)
    weighted_tf = np.divide(frequencies, words.size)
    weighted_tf = np.log(weighted_tf)
    weighted_tf = np.add(weighted_tf, 1)
    df = pd.DataFrame({"Terms": terms, "Count": frequencies, "TF": weighted_tf})
    return df


def inverse_document_frequency() -> pd.DataFrame:
    """
    Compute the weighted inverse document frequency.

    Term Count, `TC`: Total number of distinct keywords.

    Reference Count, `RC(w)`: Number of distinct documents that contain w.

    `Weighted IDF(w) = ln(1 + TC / RC(w))`

    Parameters
    ----------
        ref_count: dict[str, int]
            Dictionary mapping a keyword to the number of documents containing it.

    Returns
    -------
        pandas.DataFrame
            Data frame with 3 columns: `Terms`, `Reference Count`, `IDF`.
            `Terms` is the word in the key set of `ref_count`.
            `Reference Count` is the number of documents containing the keyword.
            `IDF` is the inverse document frequency of the keyword.
            Data frame is sorted on `Terms` column.
    """

    terms = []
    tf_files = [file for file in os.listdir(env.METADATATA_PATH) if file != env.IDF_CSV]
    for file in tf_files:
        tf_df = pd.read_csv(f"{env.METADATATA_PATH}/{file}")
        terms.extend(tf_df["Terms"].to_list())
    terms, ref_count = np.unique(terms, return_counts=True)
    weighted_idf = [terms.size] * terms.size
    weighted_idf = np.divide(weighted_idf, ref_count)
    weighted_idf = np.log1p(weighted_idf)
    df = pd.DataFrame(
        {"Terms": terms, "Reference Count": ref_count, "IDF": weighted_idf}
    )
    return df
