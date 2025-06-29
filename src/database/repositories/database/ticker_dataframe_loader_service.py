"""Service for loading ticker data as DataFrame from database."""

import logging
import pandas as pd
from sqlalchemy import create_engine


class TickerDataFrameLoaderService:
    """Service responsible only for loading ticker data as DataFrame from database."""

    def __init__(self, database_url: str):
        """
        Initialize the ticker dataframe loader service.

        Args:
            database_url: Database connection URL
        """
        self.database_url = database_url

    def load_tickers_dataframe(self) -> pd.DataFrame:
        """
        Load ticker data as a pandas DataFrame.

        Returns:
            DataFrame with ticker data
        """
        try:
            engine = create_engine(self.database_url)
            with engine.connect() as connection:
                return pd.read_sql("SELECT ticker, title FROM tickers", connection)

        except Exception as e:
            logging.error("Error loading tickers from database: %s", e)
            return pd.DataFrame(columns=["ticker", "title"])
