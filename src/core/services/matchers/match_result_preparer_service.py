"""Service for preparing final match results."""

import logging
import pandas as pd
from typing import Tuple, List, Dict


class MatchResultPreparerService:
    """Service responsible only for preparing final match results."""

    def prepare_match_results(self, candidates_with_scores: List[Dict]) -> Tuple:
        """
        Prepare final match results from scored candidates.

        Args:
            candidates_with_scores: List of candidates with scores

        Returns:
            Tuple with formatted match results
        """
        # Sort by combined score
        candidates_with_scores.sort(key=lambda x: x["combined_score"], reverse=True)

        # Get the best match
        best_candidate = candidates_with_scores[0]
        best_row = best_candidate["row"]

        ticker = best_row["ticker"] if pd.notnull(best_row["ticker"]) else None

        # Prepare results
        all_possible_tickers = []
        top_matches = []

        # If the best match has a perfect score (100), only return that single match
        is_perfect_match = best_candidate["combined_score"] >= 100.0

        max_candidates = 1 if is_perfect_match else len(candidates_with_scores)

        for i, candidate in enumerate(candidates_with_scores[:max_candidates]):
            row = candidate["row"]
            t = row["ticker"]

            if pd.notnull(t):
                all_possible_tickers.append(t)

                # Log combined scoring details
                logging.info(
                    "Combined score: %s (Fuzzy: %s, Vector: %s)",
                    candidate["combined_score"],
                    candidate["fuzzy_score"],
                    candidate["vector_score"],
                )

                top_matches.append(
                    {
                        "Rank": i + 1,
                        "company_name": row["title"],
                        "ticker": t,
                        "name_match_score": candidate["combined_score"],
                    }
                )

        if is_perfect_match:
            logging.info(
                "Perfect match found (score=%.1f), returning single result only",
                best_candidate["combined_score"],
            )

        # Remove duplicates while preserving order
        all_possible_tickers = list(dict.fromkeys(all_possible_tickers))

        return (
            best_row["title"],
            ticker,
            all_possible_tickers,
            best_candidate["combined_score"],
            None,
            top_matches,
        )
