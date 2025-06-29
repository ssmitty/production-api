"""Service for checking ticker service health."""

import logging
from src.core.services.raw_data_fetcher_service import RawDataFetcherService


class TickerHealthCheckerService:
    """Service responsible only for checking ticker service health."""

    def __init__(self, data_fetcher: RawDataFetcherService):
        """
        Initialize the ticker health checker service.

        Args:
            data_fetcher: Service for fetching raw data
        """
        self.data_fetcher = data_fetcher

    def check_health(self) -> bool:
        """
        Check if the ticker service and its dependencies are healthy.

        Returns:
            True if all services are healthy, False otherwise
        """
        try:
            # Check if data fetcher service is healthy
            return self.data_fetcher.health_check()
        except Exception as e:
            logging.error("Ticker service health check failed: %s", e)
            return False
