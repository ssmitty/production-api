"""Service for fetching ticker data as objects."""

import pandas as pd
from typing import List
from src.models.ticker import TickerData
from src.core.services.raw_data_fetcher_service import RawDataFetcherService
from src.core.services.data_processing.raw_data_processor_service import (
    RawDataProcessorService,
)
from src.core.services.functions.converters import convert_to_ticker_objects


class TickerDataFetcherService:
    """Service responsible only for fetching ticker data as objects."""

    def __init__(
        self,
        data_fetcher: RawDataFetcherService,
        raw_data_processor: RawDataProcessorService,
    ):
        """
        Initialize the ticker data fetcher service.

        Args:
            data_fetcher: Service for fetching raw data
            raw_data_processor: Service for processing raw data
            Note: Converter is now an async function instead of a class
        """
        self.data_fetcher = data_fetcher
        self.raw_data_processor = raw_data_processor

    async def fetch_ticker_objects(self) -> List[TickerData]:
        """
        Fetch and process ticker data as objects.

        Returns:
            List of TickerData objects
        """
        # Fetch raw data
        raw_df = self.data_fetcher.fetch_listing_data()

        # Process the data
        processed_df = await self.raw_data_processor.process_raw_ticker_data(raw_df)

        # Convert to TickerData objects
        return await convert_to_ticker_objects(processed_df)
