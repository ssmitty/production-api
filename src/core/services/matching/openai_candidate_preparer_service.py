"""Service responsible only for preparing OpenAI candidates."""

from typing import List, Dict
import pandas as pd


class OpenAICandidatePreparerService:
    """Service responsible only for preparing candidates for OpenAI fallback matching."""

    def prepare_openai_candidates(
        self, fallback_matches: List, tickers_df: pd.DataFrame
    ) -> List[Dict]:
        """
        Prepare candidates for OpenAI fallback matching.

        Args:
            fallback_matches: List of fallback matches from fuzzy search
            tickers_df: DataFrame with ticker data

        Returns:
            List of candidate dictionaries for OpenAI
        """
        candidates = []
        for m in fallback_matches:
            row = tickers_df[tickers_df["preprocessed_title"] == m[0]]
            if not row.empty:
                candidates.append(
                    {
                        "company_name": row.iloc[0]["title"],
                        "ticker": row.iloc[0]["ticker"],
                        "score": m[1],
                    }
                )
        return candidates
