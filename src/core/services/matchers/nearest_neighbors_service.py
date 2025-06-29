"""Service responsible only for nearest neighbors model."""

from typing import Optional
from sklearn.neighbors import NearestNeighbors
from src.config.settings import settings


class NearestNeighborsService:
    """Service responsible only for nearest neighbors model."""

    def __init__(self):
        """Initialize the nearest neighbors service."""
        self._neighbors_model: Optional[NearestNeighbors] = None

    def create_and_fit_neighbors(self, vectorized_titles):
        """
        Create and fit nearest neighbors model with vectorized data.

        Args:
            vectorized_titles: Vectorized representation of titles

        Returns:
            Fitted NearestNeighbors model
        """
        self._neighbors_model = NearestNeighbors(
            n_neighbors=settings.ML_NEIGHBORS_COUNT, metric="cosine"
        )
        self._neighbors_model.fit(vectorized_titles)
        return self._neighbors_model

    def get_neighbors_model(self) -> Optional[NearestNeighbors]:
        """
        Get the fitted neighbors model.

        Returns:
            Fitted NearestNeighbors model or None if not fitted yet
        """
        return self._neighbors_model
