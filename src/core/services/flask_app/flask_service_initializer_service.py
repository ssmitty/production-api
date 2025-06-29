"""Service responsible only for initializing Flask application services."""

import logging
from typing import Optional

from src.config.settings import settings
from src.core.services.openai_service import OpenAIService
from src.core.services.company_matcher_service import CompanyMatcherService
from src.core.services.ticker_updater_service import TickerUpdaterService
from src.database.repositories.database import (
    TickerDataFrameLoaderService,
    TickerDataFrameSaverService,
    MetadataService,
    DatabaseHealthService,
)


class FlaskServiceInitializerService:
    """Service responsible only for initializing Flask application services."""

    def __init__(self, database_url: str, openai_api_key: Optional[str] = None):
        """
        Initialize the Flask service initializer.

        Args:
            database_url: PostgreSQL database connection URL (required)
            openai_api_key: OpenAI API key (optional)
        """
        if not database_url:
            raise ValueError("database_url is required")

        self.database_url = database_url
        self.openai_api_key = openai_api_key

        # Initialize service containers
        self.dataframe_loader = None
        self.dataframe_saver = None
        self.metadata_service = None
        self.health_service = None
        self.openai_service = None
        self.company_matcher = None
        self.ticker_updater = None

    def initialize_services(self) -> None:
        """
        Initialize all Flask application services.
        """
        # Database micro-services
        self.dataframe_loader = TickerDataFrameLoaderService(self.database_url)
        self.dataframe_saver = TickerDataFrameSaverService(self.database_url)
        self.metadata_service = MetadataService(self.database_url)
        self.health_service = DatabaseHealthService(self.database_url)

        # OpenAI service (optional - may be None if API key not provided)
        if self.openai_api_key:
            try:
                self.openai_service = OpenAIService(self.openai_api_key)
                logging.info("OpenAI service initialized successfully")
            except Exception as e:
                logging.warning("Failed to initialize OpenAI service: %s", e)

        # Company matcher service - pass the dataframe loader
        self.company_matcher = CompanyMatcherService(
            dataframe_loader=self.dataframe_loader, openai_service=self.openai_service
        )

        # Ticker updater service
        self.ticker_updater = TickerUpdaterService()

        logging.info("All Flask services initialized successfully")
