"""Service for orchestrating ticker data update process."""

import pandas as pd
from typing import List, Optional
from src.models.ticker import TickerData
from src.core.services.raw_data_fetcher_service import RawDataFetcherService
from src.core.services.data_processing.raw_data_processor_service import (
    RawDataProcessorService,
)

from src.core.services.data_processing.ticker_data_fetcher_service import (
    TickerDataFetcherService,
)
from src.core.services.data_processing.ticker_dataframe_fetcher_service import (
    TickerDataFrameFetcherService,
)
from src.core.services.health_checkers.ticker_health_checker_service import (
    TickerHealthCheckerService,
)


class TickerUpdaterService:
    """Service for orchestrating the ticker data update process."""

    def __init__(
        self,
        api_key: str,
        data_fetcher: Optional[RawDataFetcherService] = None,
        raw_data_processor: Optional[RawDataProcessorService] = None,
        ticker_data_fetcher: Optional[TickerDataFetcherService] = None,
        ticker_dataframe_fetcher: Optional[TickerDataFrameFetcherService] = None,
        health_checker: Optional[TickerHealthCheckerService] = None,
    ):
        """
        Initialize the ticker updater service.

        Args:
            api_key: Alpha Vantage API key
            data_fetcher: Service for fetching raw data
            raw_data_processor: Service for processing raw data
            ticker_data_fetcher: Service for fetching ticker objects
            ticker_dataframe_fetcher: Service for fetching ticker DataFrame
            health_checker: Service for health checking
        """
        self.data_fetcher = data_fetcher or RawDataFetcherService(api_key=api_key)
        self.raw_data_processor = raw_data_processor or RawDataProcessorService()
        self.ticker_data_fetcher = ticker_data_fetcher or TickerDataFetcherService(
            self.data_fetcher, self.raw_data_processor
        )
        self.ticker_dataframe_fetcher = (
            ticker_dataframe_fetcher
            or TickerDataFrameFetcherService(self.data_fetcher, self.raw_data_processor)
        )
        self.health_checker = health_checker or TickerHealthCheckerService(
            self.data_fetcher
        )

    async def fetch_ticker_data(self) -> List[TickerData]:
        """
        Fetch and process ticker data from Alpha Vantage API.

        Returns:
            List of TickerData objects
        """
        return await self.ticker_data_fetcher.fetch_ticker_objects()

    async def fetch_ticker_dataframe(self) -> pd.DataFrame:
        """
        Fetch and process ticker data as a DataFrame.

        Returns:
            Processed ticker DataFrame
        """
        return await self.ticker_dataframe_fetcher.fetch_ticker_dataframe()

    def health_check(self) -> bool:
        """
        Check if the service and its dependencies are healthy.

        Returns:
            True if all services are healthy, False otherwise
        """
        return self.health_checker.check_health()
