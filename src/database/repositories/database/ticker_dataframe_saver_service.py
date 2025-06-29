"""Service for saving ticker DataFrame to database."""

import logging
import pandas as pd
from typing import Optional
from sqlalchemy import create_engine
from .metadata_service import MetadataService


class TickerDataFrameSaverService:
    """Service responsible only for saving ticker DataFrame to database."""

    def __init__(
        self, database_url: str, metadata_service: Optional[MetadataService] = None
    ):
        """
        Initialize the ticker dataframe saver service.

        Args:
            database_url: Database connection URL
            metadata_service: Service for updating metadata
        """
        self.database_url = database_url
        self.metadata_service = metadata_service or MetadataService(database_url)

    def save_tickers_dataframe(self, df: pd.DataFrame) -> None:
        """
        Save ticker DataFrame to the database.

        Args:
            df: DataFrame with ticker and title columns
        """
        try:
            engine = create_engine(self.database_url)
            df.to_sql("tickers", engine, if_exists="replace", index=False)

            # Update metadata
            self.metadata_service.update_last_updated()

            logging.info("Successfully saved %d tickers to database", len(df))

        except Exception as e:
            logging.error("Error saving tickers to database: %s", e)
            raise
