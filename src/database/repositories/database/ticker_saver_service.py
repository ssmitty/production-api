"""Service for saving ticker objects to database."""

import logging
import pandas as pd
from typing import List, Optional
from sqlalchemy import create_engine
from src.models.ticker import TickerData
from .metadata_service import MetadataService


class TickerSaverService:
    """Service responsible only for saving ticker objects to database."""

    def __init__(
        self, database_url: str, metadata_service: Optional[MetadataService] = None
    ):
        """
        Initialize the ticker saver service.

        Args:
            database_url: Database connection URL
            metadata_service: Service for updating metadata
        """
        self.database_url = database_url
        self.metadata_service = metadata_service or MetadataService(database_url)

    def save_tickers(self, ticker_data: List[TickerData]) -> None:
        """
        Save ticker data to the database.

        Args:
            ticker_data: List of TickerData objects to save
        """
        try:
            # Convert to DataFrame for bulk insert
            df = pd.DataFrame(
                [{"ticker": td.ticker, "title": td.title} for td in ticker_data]
            )

            engine = create_engine(self.database_url)
            df.to_sql("tickers", engine, if_exists="replace", index=False)

            # Update metadata
            self.metadata_service.update_last_updated()

            logging.info("Successfully saved %d tickers to database", len(ticker_data))

        except Exception as e:
            logging.error("Error saving tickers to database: %s", e)
            raise
