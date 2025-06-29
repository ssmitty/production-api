"""Service responsible only for TF-IDF vectorization."""

from typing import Optional, List
from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfVectorizerService:
    """Service responsible only for TF-IDF vectorization."""

    def __init__(self):
        """Initialize the TF-IDF vectorizer service."""
        self._vectorizer: Optional[TfidfVectorizer] = None
        self._vectorized_titles = None

    def create_and_fit_vectorizer(self, titles: List[str]):
        """
        Create and fit TF-IDF vectorizer with the given titles.

        Args:
            titles: List of preprocessed company titles

        Returns:
            Vectorized representation of titles
        """
        self._vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5))
        self._vectorized_titles = self._vectorizer.fit_transform(titles)
        return self._vectorized_titles

    def get_vectorizer(self) -> Optional[TfidfVectorizer]:
        """
        Get the fitted vectorizer.

        Returns:
            Fitted TfidfVectorizer or None if not fitted yet
        """
        return self._vectorizer
