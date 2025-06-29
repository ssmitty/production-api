"""Service for orchestrating company name matching using micro-services."""

import logging
import time
import pandas as pd
from typing import Optional

from src.models.ticker import MatchResult
from src.database.repositories.database import TickerDataFrameLoaderService
from src.core.services.matching import (
    DataPreparationService,
    StrategyOrchestratorService,
)
from src.core.services.exact_matcher_service import ExactMatcherService
from src.core.services.fuzzy_matcher_service import FuzzyMatcherService
from src.core.services.openai_service import OpenAIService


class CompanyMatcherService:
    """Service for orchestrating company name matching using micro-services."""

    def __init__(
        self,
        dataframe_loader: Optional[TickerDataFrameLoaderService] = None,
        openai_service: Optional[OpenAIService] = None,
        exact_matcher: Optional[ExactMatcherService] = None,
        fuzzy_matcher: Optional[FuzzyMatcherService] = None,
        data_preparer: Optional[DataPreparationService] = None,
        strategy_orchestrator: Optional[StrategyOrchestratorService] = None,
    ):
        """
        Initialize the company matcher service with micro-services.

        Args:
            dataframe_loader: Micro-service for loading ticker dataframes
            openai_service: OpenAI service for fallback matching
            exact_matcher: Service for exact name matching
            fuzzy_matcher: Service for fuzzy matching
            data_preparer: Service for preparing data
            strategy_orchestrator: Service for orchestrating strategies
        """
        self.dataframe_loader = dataframe_loader
        self.exact_matcher = exact_matcher or ExactMatcherService()
        self.fuzzy_matcher = fuzzy_matcher or FuzzyMatcherService()

        # Initialize micro-services
        self.data_preparer = data_preparer or DataPreparationService()
        self.strategy_orchestrator = (
            strategy_orchestrator
            or StrategyOrchestratorService(
                exact_matcher=self.exact_matcher,
                fuzzy_matcher=self.fuzzy_matcher,
                openai_service=openai_service,
            )
        )

    def match_company(self, company_name: str) -> MatchResult:
        """
        Main entry point for company name matching using micro-services.

        Args:
            company_name: The company name to match

        Returns:
            MatchResult object with match details
        """
        start_time = time.time()

        # Load ticker data using micro-service
        tickers_df = self._load_ticker_data()

        if tickers_df.empty:
            return MatchResult(
                matched_name=None,
                predicted_ticker=None,
                all_possible_tickers=[],
                name_match_score=0,
                message="No ticker data available",
                top_matches=[],
                api_latency=time.time() - start_time,
            )

        # Prepare data for matching using micro-service
        tickers_df = self.data_preparer.add_preprocessed_column(tickers_df)

        # Perform matching using orchestrated strategy micro-service (vectorization is automatic)
        result = self.strategy_orchestrator.orchestrate_matching_strategy(
            company_name, tickers_df
        )

        api_latency = time.time() - start_time

        return MatchResult(
            matched_name=result[0],
            predicted_ticker=result[1],
            all_possible_tickers=result[2],
            name_match_score=result[3],
            message=result[4],
            top_matches=result[5],
            api_latency=api_latency,
        )

    def _load_ticker_data(self) -> pd.DataFrame:
        """
        Load ticker data using micro-service.

        Returns:
            DataFrame with ticker data

        Raises:
            ValueError: If no dataframe_loader is provided
        """
        if self.dataframe_loader:
            return self.dataframe_loader.load_tickers_dataframe()
        else:
            # No fallback allowed in library-first approach - must be injected
            raise ValueError(
                "dataframe_loader is required and must be provided via constructor"
            )
