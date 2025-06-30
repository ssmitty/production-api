"""Service for processing ticker data using composition of micro-services."""

from typing import List, Optional

from src.models.ticker import TickerData
from src.core.services.data_processing.raw_data_processor_service import (
    RawDataProcessorService,
)


class TickerDataProcessorService:
    """Service responsible only for orchestrating ticker data processing."""

    def __init__(self, raw_processor: Optional[RawDataProcessorService] = None):
        """
        Initialize the ticker data processor.

        Args:
            raw_processor: Service for processing raw ticker data
        """
        self.raw_processor = raw_processor or RawDataProcessorService()

    async def process_ticker_data(self, raw_data: List[dict]) -> List[TickerData]:
        """
        Process raw ticker data into TickerData objects.

        Args:
            raw_data: List of raw ticker dictionaries

        Returns:
            List of processed TickerData objects
        """
        # Process the raw data into a DataFrame
        processed_df = await self.raw_processor.process_raw_data(raw_data)

        # Convert DataFrame to TickerData objects using the property method
        return TickerData.from_dataframe(processed_df)
