"""Service for orchestrating fuzzy matching with vector scoring."""

import pandas as pd
from typing import Tuple, Optional
from src.core.services.matchers.vectorizer_setup_service import VectorizerSetupService
from src.core.services.matchers.fuzzy_match_finder_service import (
    FuzzyMatchFinderService,
)
from src.core.services.matchers.match_score_calculator_service import (
    MatchScoreCalculatorService,
)
from src.core.services.matchers.match_result_preparer_service import (
    MatchResultPreparerService,
)


class FuzzyMatcherService:
    """Service responsible only for finding fuzzy matches with automatic vectorization setup."""

    def __init__(
        self,
        vectorizer_setup: Optional[VectorizerSetupService] = None,
        fuzzy_finder: Optional[FuzzyMatchFinderService] = None,
        score_calculator: Optional[MatchScoreCalculatorService] = None,
        result_preparer: Optional[MatchResultPreparerService] = None,
    ):
        """
        Initialize the fuzzy matcher service with micro-services.

        Args:
            vectorizer_setup: Service for setting up vectorization
            fuzzy_finder: Service for finding fuzzy matches
            score_calculator: Service for calculating scores
            result_preparer: Service for preparing results
        """
        self.vectorizer_setup = vectorizer_setup or VectorizerSetupService()
        self.fuzzy_finder = fuzzy_finder or FuzzyMatchFinderService()
        self.score_calculator = score_calculator or MatchScoreCalculatorService()
        self.result_preparer = result_preparer or MatchResultPreparerService()
        self._is_setup = False
        self._last_df_id = None

    def find_fuzzy_matches(
        self, name_processed: str, tickers_df: pd.DataFrame
    ) -> Tuple:
        """
        Find fuzzy matches using orchestrated micro-services with automatic vectorization setup.

        Args:
            name_processed: Preprocessed company name
            tickers_df: DataFrame with ticker data

        Returns:
            Tuple with match results
            Format: (matched_name, predicted_ticker, all_possible_tickers, score, message, top_matches)
        """
        # Setup vectorization if not already done or dataframe changed
        current_df_id = id(tickers_df)
        if not self._is_setup or self._last_df_id != current_df_id:
            self.vectorizer_setup.setup_vectorization(tickers_df)
            self._is_setup = True
            self._last_df_id = current_df_id

        # Get initial fuzzy matches
        title_list = tickers_df["preprocessed_title"].tolist()
        fuzzy_matches = self.fuzzy_finder.find_fuzzy_matches(name_processed, title_list)

        # Filter for strong matches
        strong_matches = self.fuzzy_finder.filter_strong_matches(fuzzy_matches)

        if not strong_matches:
            return (
                None,
                None,
                [],
                0,
                "Company is not in public company list",
                fuzzy_matches,
            )

        # Calculate combined scores using vectorizer
        candidates_with_scores = self.score_calculator.calculate_combined_scores(
            name_processed, strong_matches, tickers_df, self.vectorizer_setup.vectorizer
        )

        if not candidates_with_scores:
            return None, None, [], 0, "Company is not in public company list", []

        # Prepare and return final results
        return self.result_preparer.prepare_match_results(candidates_with_scores)
