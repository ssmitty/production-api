"""
Consolidated TickerMatcher library for engineering teams.

Simple usage:
    from ticker_matcher import TickerMatcher

    matcher = TickerMatcher(api_key="your_openai_key", database_url="your_db_url")
    result = matcher.match("Apple Inc")
    print(result)  # Returns clean dictionary
"""

import os
import sys

# Add project root to Python path for proper imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import logging
import time
from dataclasses import asdict
from typing import Optional, Dict, Any, List

import pandas as pd

# Import models
from src.models.ticker import MatchResult

# Import core services
from src.database.repositories import TickerDataFrameLoaderService
from src.core.services.exact_matcher_service import ExactMatcherService
from src.core.services.fuzzy_matcher_service import FuzzyMatcherService
from src.core.services.openai_service import OpenAIService
from src.core.services.matching import (
    DataPreparationService,
    StrategyOrchestratorService,
)
from src.config.settings import settings


class TickerMatcher:
    """
    Consolidated ticker matching service for engineering teams.

    Provides a simple interface while internally using all the micro-services.
    Follows Python best practices with proper initialization and error handling.
    """

    def __init__(
        self, database_url: str, api_key: Optional[str] = None, log_level: str = "INFO"
    ):
        """
        Initialize the TickerMatcher with required configuration.

        This is the main entry point for engineering teams to use the ticker
        matching functionality as a library.

        Args:
            database_url: PostgreSQL database connection URL (required)
            api_key: OpenAI API key for fallback matching (optional)
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        # Validate required parameters
        if not database_url:
            raise ValueError("database_url is required")

        # Setup logging
        logging.basicConfig(level=getattr(logging, log_level.upper()))
        self.logger = logging.getLogger(__name__)

        # Configuration - no os.environ usage, all passed through constructor
        self.api_key = api_key
        self.database_url = database_url

        # Initialize core services
        self._setup_services()

        # Cache for ticker data
        self._ticker_data_cache: Optional[pd.DataFrame] = None
        self._cache_timestamp: Optional[float] = None
        self._cache_ttl = 300  # 5 minutes cache TTL

        self.logger.info("TickerMatcher initialized successfully")

    def match(self, company_name: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Match a company name to its ticker symbol.

        Args:
            company_name: The company name to match
            use_cache: Whether to use cached ticker data (default: True)

        Returns:
            Dictionary with match results:
            {
                'matched_name': str or None,
                'predicted_ticker': str or None,
                'all_possible_tickers': List[str],
                'name_match_score': float,
                'message': str or None,
                'top_matches': List[dict],
                'api_latency': float,
                'success': bool
            }
        """
        try:
            start_time = time.time()

            # Validate input
            if not company_name or not isinstance(company_name, str):
                return self._error_response("Invalid company name provided", start_time)

            company_name = company_name.strip()
            if not company_name:
                return self._error_response("Empty company name provided", start_time)

            # Load ticker data
            tickers_df = self._get_ticker_data(use_cache)
            if tickers_df.empty:
                return self._error_response("No ticker data available", start_time)

            # Prepare data for matching
            tickers_df = self.data_preparer.add_preprocessed_column(tickers_df)

            # Perform matching using orchestrated strategy
            result = self.strategy_orchestrator.orchestrate_matching_strategy(
                company_name, tickers_df
            )

            # Calculate total latency
            api_latency = time.time() - start_time

            # Create and format result
            match_result = MatchResult(
                matched_name=result[0],
                predicted_ticker=result[1],
                all_possible_tickers=result[2],
                name_match_score=result[3],
                message=result[4],
                top_matches=result[5],
                api_latency=api_latency,
            )

            # Convert to dictionary and add success flag
            result_dict = asdict(match_result)
            result_dict["success"] = True

            self.logger.info(
                "Successfully matched '%s' to '%s' in %.3fs",
                company_name, result[1], api_latency
            )
            return result_dict

        except (ValueError, KeyError, AttributeError, RuntimeError) as e:
            self.logger.error("Error matching company '%s': %s", company_name, str(e))
            return self._error_response(f"Internal error: {str(e)}", start_time)

    def batch_match(
        self, company_names: List[str], use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Match multiple company names in batch.

        Args:
            company_names: List of company names to match
            use_cache: Whether to use cached ticker data

        Returns:
            List of match result dictionaries
        """
        if not isinstance(company_names, list):
            raise ValueError("company_names must be a list")

        results = []
        for company_name in company_names:
            result = self.match(company_name, use_cache)
            results.append(result)

        return results

    def health_check(self) -> Dict[str, Any]:
        """
        Check system health and dependencies.

        Returns:
            Dictionary with health status
        """
        start_time = time.time()
        health_status = {
            "status": "healthy",
            "checks": {},
            "timestamp": time.time(),
            "response_time": 0,
        }

        try:
            # Check database connection
            try:
                tickers_df = self._get_ticker_data(use_cache=False)
                health_status["checks"]["database"] = {
                    "status": "healthy" if not tickers_df.empty else "warning",
                    "records_count": len(tickers_df) if not tickers_df.empty else 0,
                }
            except (ValueError, KeyError, AttributeError, RuntimeError,
                    ConnectionError, TimeoutError) as e:
                health_status["checks"]["database"] = {
                    "status": "unhealthy",
                    "error": str(e),
                }
                health_status["status"] = "unhealthy"

            # Check OpenAI service
            if self.api_key:
                health_status["checks"]["openai"] = {"status": "configured"}
            else:
                health_status["checks"]["openai"] = {"status": "not_configured"}

            # Check core services
            health_status["checks"]["services"] = {
                "exact_matcher": "initialized",
                "fuzzy_matcher": "initialized",
                "data_preparer": "initialized",
                "strategy_orchestrator": "initialized",
            }

        except (ValueError, KeyError, AttributeError, RuntimeError,
                ConnectionError, TimeoutError) as e:
            health_status["status"] = "unhealthy"
            health_status["error"] = str(e)

        health_status["response_time"] = time.time() - start_time
        return health_status

    def clear_cache(self) -> None:
        """Clear the ticker data cache."""
        self._ticker_data_cache = None
        self._cache_timestamp = None
        self.logger.info("Ticker data cache cleared")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get matcher statistics and configuration.

        Returns:
            Dictionary with current stats and config
        """
        return {
            "cache_enabled": self._ticker_data_cache is not None,
            "cache_age_seconds": (
                time.time() - self._cache_timestamp if self._cache_timestamp else None
            ),
            "cache_ttl_seconds": self._cache_ttl,
            "openai_configured": bool(self.api_key),
            "database_configured": bool(self.database_url),
            "services_initialized": {
                "exact_matcher": self.exact_matcher is not None,
                "fuzzy_matcher": self.fuzzy_matcher is not None,
                "openai_service": self.openai_service is not None,
                "dataframe_loader": self.dataframe_loader is not None,
            },
        }

    def _setup_services(self) -> None:
        """Initialize all internal services."""
        try:
            # Initialize database loader
            if self.database_url:
                self.dataframe_loader = TickerDataFrameLoaderService(self.database_url)
            else:
                self.dataframe_loader = None
                self.logger.warning(
                    "No database URL provided, some features may be limited"
                )

            # Initialize OpenAI service
            if self.api_key:
                self.openai_service = OpenAIService(self.api_key)
            else:
                self.openai_service = None
                self.logger.info(
                    "No OpenAI API key provided, fallback matching disabled"
                )

            # Initialize matching services
            self.exact_matcher = ExactMatcherService()
            self.fuzzy_matcher = FuzzyMatcherService()

            # Initialize orchestration services
            self.data_preparer = DataPreparationService()
            self.strategy_orchestrator = StrategyOrchestratorService(
                exact_matcher=self.exact_matcher,
                fuzzy_matcher=self.fuzzy_matcher,
                openai_service=self.openai_service,
            )

        except (ValueError, KeyError, AttributeError, RuntimeError,
                ImportError, ModuleNotFoundError) as e:
            self.logger.error("Failed to initialize services: %s", str(e))
            raise

    def _get_ticker_data(self, use_cache: bool = True) -> pd.DataFrame:
        """
        Get ticker data with optional caching.

        Args:
            use_cache: Whether to use cached data

        Returns:
            DataFrame with ticker data
        """
        # Check cache validity
        if (
            use_cache
            and self._ticker_data_cache is not None
            and self._cache_timestamp is not None
            and time.time() - self._cache_timestamp < self._cache_ttl
        ):
            return self._ticker_data_cache

        # Load fresh data
        if self.dataframe_loader:
            tickers_df = self.dataframe_loader.load_tickers_dataframe()
        else:
            # Fallback: try to create temporary loader from settings
            try:
                temp_loader = TickerDataFrameLoaderService(settings.DATABASE_URL)
                tickers_df = temp_loader.load_tickers_dataframe()
            except (ValueError, KeyError, AttributeError, RuntimeError,
                    ConnectionError, ImportError, ModuleNotFoundError):
                self.logger.error(
                    "Cannot load ticker data: no database connection available"
                )
                return pd.DataFrame()

        # Update cache
        if use_cache:
            self._ticker_data_cache = tickers_df
            self._cache_timestamp = time.time()

        return tickers_df

    def _error_response(self, message: str, start_time: float) -> Dict[str, Any]:
        """
        Create standardized error response.

        Args:
            message: Error message
            start_time: Request start time

        Returns:
            Error response dictionary
        """
        return {
            "matched_name": None,
            "predicted_ticker": None,
            "all_possible_tickers": [],
            "name_match_score": 0.0,
            "message": message,
            "top_matches": [],
            "api_latency": time.time() - start_time,
            "success": False,
        }


if __name__ == "__main__":
    """
    Example usage of the TickerMatcher library.
    
    This demonstrates how engineering teams can use the TickerMatcher 
    as a standalone library in their projects.
    """
    import os
    
    # Get database URL from environment (required)
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("❌ ERROR: DATABASE_URL environment variable is required")
        print("Please set your DATABASE_URL and try again:")
        print("export DATABASE_URL='postgresql://username:password@host:port/database'")
        sys.exit(1)
    
    # Get OpenAI API key (optional)
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    
    try:
        print("🔄 Initializing TickerMatcher library...")
        
        # Initialize the TickerMatcher
        matcher = TickerMatcher(
            database_url=database_url,
            api_key=openai_api_key,
            log_level="INFO"
        )
        
        print("✅ TickerMatcher initialized successfully!")
        print()
        
        # Perform health check
        print("🔄 Performing health check...")
        health = matcher.health_check()
        print(f"Health Status: {health['status']}")
        print(f"Database: {health['checks']['database']['status']}")
        if health['checks']['database']['status'] == 'healthy':
            print(f"Records Count: {health['checks']['database']['records_count']}")
        print()
        
        # Example company matches
        test_companies = [
            "Apple Inc",
            "Microsoft Corporation", 
            "Tesla",
            "Google",
            "Amazon"
        ]
        
        print("🔄 Running example matches...")
        print("-" * 50)
        
        for company in test_companies:
            print(f"Matching: {company}")
            result = matcher.match(company)
            
            if result['success']:
                print(f"✅ Result: {result['predicted_ticker']} ({result['matched_name']})")
                print(f"   Score: {result['name_match_score']:.1f}%")
                print(f"   Latency: {result['api_latency']:.3f}s")
            else:
                print(f"❌ Failed: {result['message']}")
            print()
        
        # Show statistics
        print("📊 Matcher Statistics:")
        stats = matcher.get_stats()
        print(f"Cache Enabled: {stats['cache_enabled']}")
        print(f"OpenAI Configured: {stats['openai_configured']}")
        print(f"Database Configured: {stats['database_configured']}")
        
        print("\n✅ Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running example: {e}")
        sys.exit(1)
