"""Data models for ticker-related entities."""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import pandas as pd


@dataclass
class TickerData:
    """Model for ticker data."""

    ticker: str
    title: str

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> List["TickerData"]:
        """
        Convert DataFrame to list of TickerData objects.

        Args:
            df: DataFrame with ticker and title columns

        Returns:
            List of TickerData objects
        """
        return [
            cls(ticker=row["ticker"], title=row["title"]) for _, row in df.iterrows()
        ]


@dataclass
class MatchResult:
    """Model for company name matching results."""

    matched_name: Optional[str]
    predicted_ticker: Optional[str]
    all_possible_tickers: List[str]
    name_match_score: float
    message: Optional[str]
    top_matches: List[dict]
    api_latency: float


@dataclass
class TopMatch:
    """Model for top match candidates."""

    rank: int
    company_name: str
    ticker: str
    name_match_score: float


@dataclass
class UpdateMetadata:
    """Model for update metadata."""

    last_updated: datetime
    timezone: str
    status: int
