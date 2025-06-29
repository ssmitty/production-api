"""Service for processing raw ticker data."""

import asyncio
import logging
import pandas as pd
from src.core.services.functions.data_filters import (
    filter_by_asset_type,
    standardize_columns,
    filter_etfs,
    remove_duplicates,
    clean_missing_data,
)
from src.core.services.functions.validators import validate_data


class RawDataProcessorService:
    """Service responsible only for processing raw ticker data using async functions."""

    def __init__(self):
        """
        Initialize the raw data processor.

        Note: Processing functions are now stateless async functions
        instead of injectable micro-service classes.
        """
        pass

    async def process_raw_ticker_data(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        """
        Process and filter raw ticker data using async functions pipeline.

        Args:
            raw_df: Raw DataFrame from Alpha Vantage API

        Returns:
            Processed and filtered DataFrame with ticker and title columns

        Raises:
            ValueError: If no valid ticker data remains after filtering
        """
        # Execute processing pipeline using async functions
        # Note: clean_missing_data must run BEFORE standardize_columns
        # because it expects 'symbol' and 'name' columns
        df_clean = await filter_by_asset_type(raw_df)
        df_clean = await filter_etfs(df_clean)
        df_clean = await remove_duplicates(df_clean)
        df_clean = await clean_missing_data(df_clean)
        df_clean = await standardize_columns(df_clean)

        # Validate final result
        is_valid = await validate_data(df_clean)
        if not is_valid:
            raise ValueError("No valid ticker data remains after filtering")

        logging.info("Successfully processed %d tickers.", len(df_clean))
        return df_clean[["ticker", "title"]]
