"""Service for orchestrating TF-IDF vectorization setup using micro-services."""

import pandas as pd
from typing import Optional
from sklearn.feature_extraction.text import TfidfVectorizer

from .tfidf_vectorizer_service import TfidfVectorizerService
from .nearest_neighbors_service import NearestNeighborsService


class VectorizerSetupService:
    """Service for orchestrating TF-IDF vectorization setup using micro-services."""

    def __init__(
        self,
        tfidf_service: Optional[TfidfVectorizerService] = None,
        neighbors_service: Optional[NearestNeighborsService] = None,
    ):
        """
        Initialize the vectorizer setup service with micro-services.

        Args:
            tfidf_service: Service for TF-IDF vectorization
            neighbors_service: Service for nearest neighbors model
        """
        self.tfidf_service = tfidf_service or TfidfVectorizerService()
        self.neighbors_service = neighbors_service or NearestNeighborsService()
        self._vectorized_titles = None

    def setup_vectorization(self, tickers_df: pd.DataFrame) -> None:
        """
        Setup TF-IDF vectorization and nearest neighbors model using micro-services.

        Args:
            tickers_df: DataFrame with preprocessed ticker data
        """
        titles = tickers_df["preprocessed_title"].tolist()

        # Use TF-IDF micro-service to create vectorizer
        self._vectorized_titles = self.tfidf_service.create_and_fit_vectorizer(titles)

        # Use neighbors micro-service to create neighbors model
        self.neighbors_service.create_and_fit_neighbors(self._vectorized_titles)

    @property
    def vectorizer(self) -> Optional[TfidfVectorizer]:
        """Get the fitted vectorizer from micro-service."""
        return self.tfidf_service.get_vectorizer()
