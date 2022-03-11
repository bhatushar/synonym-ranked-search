import nltk
import numpy as np


def sanitize_text(text: str) -> np.ndarray:
    """
    Applies following transformation to the data:
    1. Conver to lowercase
    2. Tokenize into words
    3. Remove stopwords
    4. Remove punctuations and single letter words
    5. Lemmatize words
    6. Stem words

    Returns
    -------
        numpy.ndarray
            Array of words generated after the transformations.
    """

    words = nltk.tokenize.word_tokenize(text)
    stopwords_set = set(nltk.corpus.stopwords.words("english"))
    # Remove common words, punctuations, and single letter words
    words = [w for w in words if w not in stopwords_set and w.isalnum() and len(w) > 1]
    # Lemmatize and stem
    wordnet = nltk.stem.WordNetLemmatizer()
    words = [wordnet.lemmatize(w) for w in words]
    porter = nltk.stem.PorterStemmer()
    words = [porter.stem(w) for w in words]
    return np.array(words)
