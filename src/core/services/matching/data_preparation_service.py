"""Service responsible only for preparing data for matching operations."""

import pandas as pd
from src.utils.company_name_cleaner import preprocess_company_name


class DataPreparationService:
    """Service responsible only for preparing data for matching operations."""

    def add_preprocessed_column(self, tickers_df: pd.DataFrame) -> pd.DataFrame:
        """
        Add a preprocessed column to the tickers dataframe.

        Args:
            tickers_df: DataFrame with ticker data

        Returns:
            DataFrame with added preprocessed_title column
        """
        tickers_df["preprocessed_title"] = tickers_df["title"].apply(
            preprocess_company_name
        )
        return tickers_df
