"""Async functions for data conversion operations."""

import asyncio
from typing import List
import pandas as pd
from src.models.ticker import TickerData


async def convert_to_ticker_objects(df: pd.DataFrame) -> List[TickerData]:
    """
    Convert DataFrame to list of TickerData objects.

    Args:
        df: DataFrame with ticker and title columns

    Returns:
        List of TickerData objects
    """
    return [
        TickerData(ticker=row["ticker"], title=row["title"]) for _, row in df.iterrows()
    ]
