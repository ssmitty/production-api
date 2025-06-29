"""Service for finding exact company name matches."""

import logging
import pandas as pd
from typing import Optional, Tuple, List


class ExactMatchFinderService:
    """Service responsible only for finding exact company name matches."""

    def find_exact_match(
        self, company_name: str, tickers_df: pd.DataFrame
    ) -> Optional[Tuple]:
        """
        Find exact matches for a company name in the tickers dataframe.

        Args:
            company_name: Company name to match
            tickers_df: DataFrame with ticker data

        Returns:
            Tuple with match results or None if no exact match found
            Format: (matched_name, predicted_ticker, all_possible_tickers, score, message, top_matches)
        """
        exact_matches = tickers_df[
            tickers_df["title"].str.lower() == company_name.lower()
        ]

        if exact_matches.empty:
            return None

        exact_tickers = []
        top_matches = []

        # For exact matches, only return the first/best match to avoid confusion
        # Since it's a perfect match, multiple options aren't helpful
        first_match = exact_matches.iloc[0]
        ticker = first_match.get("ticker")

        if pd.notnull(ticker):
            exact_tickers.append(ticker)
        else:
            logging.warning("No ticker found for company: %s", company_name)

        top_matches.append(
            {
                "Rank": 1,
                "company_name": first_match["title"],
                "ticker": ticker,
                "name_match_score": 100.0,
            }
        )
        
        logging.info("🎯 Exact match found for '%s', returning single result only", company_name)

        # Return appropriate response based on ticker availability
        if not exact_tickers:
            return (
                first_match["title"],
                None,
                [],
                100.0,
                "No ticker found for company",
                top_matches,
            )

        return (
            first_match["title"],
            exact_tickers[0],  # Primary ticker
            exact_tickers,  # All possible tickers
            100.0,  # Perfect score for exact match
            None,  # No error message
            top_matches,
        )
