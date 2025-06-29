"""Service for fetching ticker data as DataFrame."""

import pandas as pd
from src.core.services.raw_data_fetcher_service import RawDataFetcherService
from src.core.services.data_processing.raw_data_processor_service import (
    RawDataProcessorService,
)


class TickerDataFrameFetcherService:
    """Service responsible only for fetching ticker data as DataFrame."""

    def __init__(
        self,
        data_fetcher: RawDataFetcherService,
        raw_data_processor: RawDataProcessorService,
    ):
        """
        Initialize the ticker dataframe fetcher service.

        Args:
            data_fetcher: Service for fetching raw data
            raw_data_processor: Service for processing raw data
        """
        self.data_fetcher = data_fetcher
        self.raw_data_processor = raw_data_processor

    async def fetch_ticker_dataframe(self) -> pd.DataFrame:
        """
        Fetch and process ticker data as DataFrame.

        Returns:
            Processed ticker DataFrame
        """
        # Fetch raw data
        raw_df = self.data_fetcher.fetch_listing_data()

        # Process and return the data
        return await self.raw_data_processor.process_raw_ticker_data(raw_df)
