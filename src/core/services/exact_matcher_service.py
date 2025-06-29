"""Service for orchestrating exact company name matching."""

import pandas as pd
from typing import Optional, Tuple
from src.core.services.matchers.exact_match_finder_service import (
    ExactMatchFinderService,
)


class ExactMatcherService:
    """Service responsible only for finding exact matches."""

    def __init__(self, match_finder: Optional[ExactMatchFinderService] = None):
        """
        Initialize the exact matcher service with micro-services.

        Args:
            match_finder: Service for finding exact matches
            Note: Validation methods moved to ExactMatchValidatorService
        """
        self.match_finder = match_finder or ExactMatchFinderService()

    def find_exact_match(
        self, company_name: str, tickers_df: pd.DataFrame
    ) -> Optional[Tuple]:
        """
        Find exact matches using the exact match finder service.

        Args:
            company_name: Company name to match
            tickers_df: DataFrame with ticker data

        Returns:
            Tuple with match results or None if no exact match found
        """
        return self.match_finder.find_exact_match(company_name, tickers_df)
