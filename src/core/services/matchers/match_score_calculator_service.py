"""Service for calculating match scores."""

import pandas as pd
from typing import List, Tuple, Dict, Optional
from sklearn.feature_extraction.text import TfidfVectorizer


class MatchScoreCalculatorService:
    """Service responsible only for calculating combined match scores."""

    def calculate_combined_scores(
        self,
        name_processed: str,
        strong_matches: List[Tuple],
        tickers_df: pd.DataFrame,
        vectorizer: Optional[TfidfVectorizer],
    ) -> List[Dict]:
        """
        Calculate combined scores using fuzzy and vector similarity.

        Args:
            name_processed: Preprocessed query name
            strong_matches: List of strong fuzzy matches
            tickers_df: DataFrame with ticker data
            vectorizer: Fitted TF-IDF vectorizer

        Returns:
            List of candidates with combined scores
        """
        candidates_with_scores = []

        if vectorizer is None:
            return self._fallback_to_fuzzy_only(strong_matches, tickers_df)

        # Get vectorizer score for the input
        query_vec = vectorizer.transform([name_processed])

        for company, fuzzy_score in strong_matches:
            # Find matching rows for this company
            matched_rows = tickers_df[tickers_df["preprocessed_title"] == company]

            if not matched_rows.empty:
                # Calculate vector similarity
                company_vec = vectorizer.transform([company])
                vector_score = float(query_vec.dot(company_vec.T).toarray()[0][0])

                for _, row in matched_rows.iterrows():
                    vector_score_scaled = round(vector_score * 100, 1)
                    # Average of fuzzy and vector scores
                    combined_score = round((fuzzy_score + vector_score_scaled) / 2, 1)

                    candidates_with_scores.append(
                        {
                            "row": row,
                            "fuzzy_score": fuzzy_score,
                            "vector_score": vector_score_scaled,
                            "combined_score": combined_score,
                            "company_name": company,
                        }
                    )

        return candidates_with_scores

    def _fallback_to_fuzzy_only(
        self, strong_matches: List[Tuple], tickers_df: pd.DataFrame
    ) -> List[Dict]:
        """
        Fallback to fuzzy scores only when vectorizer is not available.

        Args:
            strong_matches: List of strong fuzzy matches
            tickers_df: DataFrame with ticker data

        Returns:
            List of candidates with fuzzy scores only
        """
        candidates = []
        for company, fuzzy_score in strong_matches:
            matched_rows = tickers_df[tickers_df["preprocessed_title"] == company]

            for _, row in matched_rows.iterrows():
                candidates.append(
                    {
                        "row": row,
                        "fuzzy_score": fuzzy_score,
                        "vector_score": 0,  # No vector score available
                        "combined_score": fuzzy_score,  # Use fuzzy score only
                        "company_name": company,
                    }
                )

        return candidates
