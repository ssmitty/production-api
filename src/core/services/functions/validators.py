"""Async functions for validation operations."""

import asyncio
import pandas as pd


async def has_exact_match(company_name: str, tickers_df: pd.DataFrame) -> bool:
    """
    Check if an exact match exists for the company name.

    Args:
        company_name: Company name to check
        tickers_df: DataFrame with ticker data

    Returns:
        True if exact match exists, False otherwise
    """
    exact_matches = tickers_df[tickers_df["title"].str.lower() == company_name.lower()]
    return not exact_matches.empty


async def count_exact_matches(company_name: str, tickers_df: pd.DataFrame) -> int:
    """
    Count the number of exact matches for the company name.

    Args:
        company_name: Company name to check
        tickers_df: DataFrame with ticker data

    Returns:
        Number of exact matches found
    """
    exact_matches = tickers_df[tickers_df["title"].str.lower() == company_name.lower()]
    return len(exact_matches)


async def validate_data(df: pd.DataFrame) -> bool:
    """
    Validate that the DataFrame has the required structure and data.

    Args:
        df: DataFrame to validate

    Returns:
        True if data is valid, False otherwise
    """
    # Check if DataFrame is empty
    if df.empty:
        return False

    # Check for required columns
    required_columns = ["ticker", "title"]
    if not all(col in df.columns for col in required_columns):
        return False

    # Check for any data in required columns
    if df[required_columns].isnull().all().any():
        return False

    return True
