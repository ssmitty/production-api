"""Async functions for data filtering operations."""

import asyncio
import logging
import pandas as pd
from typing import List
from src.utils.etf_detector import filter_etfs as detect_etfs


async def filter_by_asset_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter DataFrame to include only stocks.

    Args:
        df: DataFrame with assetType column

    Returns:
        DataFrame filtered to stocks only
    """
    if "assetType" in df.columns:
        df_filtered = df[df["assetType"] == "Stock"].copy()
        logging.info(
            "Filtered to %d stocks from %d total records.", len(df_filtered), len(df)
        )
    else:
        logging.warning(
            "'assetType' column not found, proceeding without assetType filter."
        )
        df_filtered = df.copy()

    return df_filtered


async def filter_etfs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter out ETFs from the DataFrame based on company name keywords.

    Args:
        df: DataFrame with 'name' column

    Returns:
        DataFrame with ETFs filtered out
    """
    if "name" not in df.columns:
        logging.warning("'name' column not found, proceeding without ETF filter.")
        return df.copy()

    # Use the ETF detection utility
    etf_flags = detect_etfs(df["name"].tolist())

    # Create boolean Series with same index as DataFrame
    etf_series = pd.Series(etf_flags, index=df.index)

    # Filter out ETFs (keep non-ETFs)
    df_filtered = df[~etf_series].copy()
    etfs_removed = len(df) - len(df_filtered)

    logging.info("Filtered out %d ETFs from %d total records.", etfs_removed, len(df))
    return df_filtered


async def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate ticker entries from DataFrame.

    Args:
        df: DataFrame with ticker data

    Returns:
        DataFrame with duplicates removed
    """
    initial_count = len(df)
    df_deduplicated = df.drop_duplicates().copy()
    duplicates_removed = initial_count - len(df_deduplicated)

    logging.info(
        "Removed %d duplicate records from %d total records.",
        duplicates_removed,
        initial_count,
    )
    return df_deduplicated


async def clean_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean missing or invalid data from DataFrame.

    Args:
        df: DataFrame with ticker data

    Returns:
        DataFrame with missing data cleaned
    """
    initial_count = len(df)

    # Remove rows where critical columns are missing
    df_cleaned = df.dropna(subset=["symbol", "name"]).copy()

    cleaned_count = initial_count - len(df_cleaned)
    logging.info(
        "Cleaned %d records with missing data from %d total records.",
        cleaned_count,
        initial_count,
    )

    return df_cleaned


async def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names for consistency.

    Args:
        df: DataFrame with ticker data

    Returns:
        DataFrame with standardized column names
    """
    # Rename columns to standard format
    df_standardized = df.rename(columns={"symbol": "ticker", "name": "title"}).copy()

    logging.info("Standardized column names for %d records.", len(df_standardized))
    return df_standardized
