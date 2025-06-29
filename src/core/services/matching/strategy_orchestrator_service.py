"""Service responsible only for orchestrating matching strategies."""

import logging
from typing import Tuple, Optional
import pandas as pd

from src.utils.company_name_cleaner import preprocess_company_name
from src.core.services.exact_matcher_service import ExactMatcherService
from src.core.services.fuzzy_matcher_service import FuzzyMatcherService
from src.core.services.openai_service import OpenAIService


class StrategyOrchestratorService:
    """Service responsible only for orchestrating matching strategies."""

    def __init__(
        self,
        exact_matcher: Optional[ExactMatcherService] = None,
        fuzzy_matcher: Optional[FuzzyMatcherService] = None,
        openai_service: Optional[OpenAIService] = None,
    ):
        """
        Initialize the strategy orchestrator.

        Args:
            exact_matcher: Service for exact name matching
            fuzzy_matcher: Service for fuzzy matching
            openai_service: OpenAI service for fallback matching
        """
        self.exact_matcher = exact_matcher or ExactMatcherService()
        self.fuzzy_matcher = fuzzy_matcher or FuzzyMatcherService()
        self.openai_service = openai_service

    def orchestrate_matching_strategy(
        self, name: str, tickers_df: pd.DataFrame
    ) -> Tuple:
        """
        Orchestrate the matching strategy using specialized services.

        Args:
            name: Company name to match
            tickers_df: DataFrame with ticker data

        Returns:
            Tuple with match results
        """
        if not isinstance(name, str):
            logging.warning("Input name is not a string: %s", name)
            return None, None, [], 0, "Company is not in public company list", []

        # 1. Try exact matching first
        exact_result = self.exact_matcher.find_exact_match(name, tickers_df)
        if exact_result:
            return exact_result

        # 2. Try fuzzy matching
        name_processed = preprocess_company_name(name)
        fuzzy_result = self.fuzzy_matcher.find_fuzzy_matches(name_processed, tickers_df)

        if fuzzy_result[0] is not None:
            return fuzzy_result

        # 3. Try OpenAI fallback if available
        if self.openai_service and self.openai_service.is_available():
            from src.core.services.matching.openai_candidate_preparer_service import (
                OpenAICandidatePreparerService,
            )
            from src.core.services.matching.openai_fallback_service import (
                OpenAIFallbackService,
            )

            candidate_preparer = OpenAICandidatePreparerService()
            fallback_service = OpenAIFallbackService(self.openai_service)

            fallback_matches = fuzzy_result[
                5
            ]  # Get the fallback matches from fuzzy result
            candidates = candidate_preparer.prepare_openai_candidates(
                fallback_matches, tickers_df
            )
            return fallback_service.try_openai_fallback(name, candidates)

        return None, None, [], 0, "Company is not in public company list", []
