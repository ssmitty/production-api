"""Abstract interface for company matching strategies."""

from abc import ABC, abstractmethod
from typing import Optional, Tuple, Dict, Any

import pandas as pd


class MatchingStrategy(ABC):
    """Abstract base class for company matching strategies."""

    @abstractmethod
    def setup(self, tickers_df: pd.DataFrame) -> None:
        """Setup the matching strategy with ticker data."""
        pass

    @abstractmethod
    def find_matches(
        self, company_name: str, tickers_df: pd.DataFrame
    ) -> Optional[Tuple]:
        """
        Find matches for a company name.

        Returns:
            Tuple with match results or None if no match found
        """
        pass

    @abstractmethod
    def get_match_confidence(self, company_name: str, matched_name: str) -> float:
        """Get confidence score for a match."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this matching strategy is available."""
        pass


class DataLoader(ABC):
    """Abstract interface for data loading operations."""

    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """Load data from source."""
        pass

    @abstractmethod
    def is_healthy(self) -> bool:
        """Check if data source is healthy."""
        pass

    @abstractmethod
    def get_last_update(self) -> Dict[str, Any]:
        """Get information about last data update."""
        pass


class DataProcessor(ABC):
    """Abstract interface for data processing operations."""

    @abstractmethod
    def process_data(self, raw_data: Any) -> pd.DataFrame:
        """Process raw data into structured format."""
        pass

    @abstractmethod
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Validate processed data."""
        pass

    @abstractmethod
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get statistics about data processing."""
        pass
