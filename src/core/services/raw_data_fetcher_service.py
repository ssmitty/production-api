"""Service for fetching raw data from external APIs."""

import io
import logging
from typing import Optional

import pandas as pd
import requests

from src.config.settings import settings


class RawDataFetcherService:
    """Service responsible only for fetching raw data from Alpha Vantage API."""

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize the raw data fetcher service.

        Args:
            api_key: Alpha Vantage API key (required)
            base_url: Base URL for Alpha Vantage API (optional, defaults to Alpha Vantage)
        """
        if not api_key:
            raise ValueError("Alpha Vantage API key is required")

        self.api_key = api_key
        self.base_url = base_url or settings.ALPHA_VANTAGE_BASE_URL

    def fetch_listing_data(self) -> pd.DataFrame:
        """
        Fetch raw listing data from Alpha Vantage API.

        Returns:
            Raw DataFrame with all listing data as returned by the API

        Raises:
            requests.RequestException: If API request fails
            pd.errors.EmptyDataError: If CSV data is invalid
        """
        api_url = f"{self.base_url}/query?function=LISTING_STATUS&apikey={self.api_key}"

        logging.info("Fetching active listings from Alpha Vantage API...")

        try:
            response = requests.get(api_url, timeout=30)
            response.raise_for_status()

            # Parse CSV response
            csv_data = response.content.decode("utf-8")
            df = pd.read_csv(
                io.StringIO(csv_data), keep_default_na=False, na_values=[""]
            )

            logging.info("Successfully fetched %d total listings from API.", len(df))
            return df

        except requests.exceptions.RequestException as e:
            logging.error("Alpha Vantage API request failed: %s", e)
            raise
        except (KeyError, pd.errors.EmptyDataError) as e:
            logging.error("Failed to process CSV data from API. Error: %s", e)
            raise

    def health_check(self) -> bool:
        """
        Check if the Alpha Vantage API is accessible.

        Returns:
            True if API is accessible, False otherwise
        """
        try:
            # Test with a simple API call
            test_url = (
                f"{self.base_url}/query?function=TIME_SERIES_INTRADAY&"
                f"symbol=AAPL&interval=1min&apikey={self.api_key}"
            )
            response = requests.get(test_url, timeout=10)
            return response.status_code == 200
        except (requests.exceptions.RequestException, ValueError) as e:
            logging.error("Alpha Vantage API health check failed: %s", e)
            return False
