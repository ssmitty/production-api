"""Service responsible only for exact match validation."""

import pandas as pd
from src.core.services.functions.validators import has_exact_match, count_exact_matches


class ExactMatchValidatorService:
    """Service responsible only for validating exact matches."""

    async def has_exact_match(
        self, company_name: str, tickers_df: pd.DataFrame
    ) -> bool:
        """
        Check if an exact match exists using the async validator function.

        Args:
            company_name: Company name to check
            tickers_df: DataFrame with ticker data

        Returns:
            True if exact match exists, False otherwise
        """
        return await has_exact_match(company_name, tickers_df)

    async def get_exact_matches_count(
        self, company_name: str, tickers_df: pd.DataFrame
    ) -> int:
        """
        Get the number of exact matches using the async validator function.

        Args:
            company_name: Company name to check
            tickers_df: DataFrame with ticker data

        Returns:
            Number of exact matches found
        """
        return await count_exact_matches(company_name, tickers_df)
