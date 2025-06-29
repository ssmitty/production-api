"""Service for loading ticker data from database."""

import logging
import pandas as pd
from typing import List
from sqlalchemy import create_engine
from src.models.ticker import TickerData


class TickerLoaderService:
    """Service responsible only for loading ticker data from database."""

    def __init__(self, database_url: str):
        """
        Initialize the ticker loader service.

        Args:
            database_url: Database connection URL
        """
        self.database_url = database_url

    def load_tickers(self) -> List[TickerData]:
        """
        Load all ticker data from the database.

        Returns:
            List of TickerData objects
        """
        try:
            engine = create_engine(self.database_url)
            with engine.connect() as connection:
                df = pd.read_sql("SELECT ticker, title FROM tickers", connection)

            return [
                TickerData(ticker=row["ticker"], title=row["title"])
                for _, row in df.iterrows()
            ]

        except Exception as e:
            logging.error("Error loading tickers from database: %s", e)
            return []
