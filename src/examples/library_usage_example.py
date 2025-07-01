"""
Example demonstrating proper dependency injection with the ticker matching service.

This shows engineering teams how to integrate the ticker matching functionality
using proper dependency injection patterns without any os.environ usage.

Usage from app_fastapi.py or other entry points:
    from src.examples.library_usage_example import TickerMatchingExample
    
    demo = TickerMatchingExample(database_url, openai_api_key)
    demo.run_full_demo()
"""

import sys
import logging

# Add the project root to the Python path for proper imports
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from src.examples.ticker_matcher import TickerMatcher

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class TickerMatchingExample:
    """Example service showing proper dependency injection patterns."""

    def __init__(self, database_url: str, openai_api_key: str = None):
        """
        Initialize with explicit dependencies (proper engineering pattern).

        Args:
            database_url: PostgreSQL database connection URL (required)
            openai_api_key: OpenAI API key for fallback matching (optional)
        """
        if not database_url:
            raise ValueError("database_url is required")
        
        self.database_url = database_url
        self.openai_api_key = openai_api_key
        
        # Initialize the ticker matcher service with dependency injection
        self.matcher = TickerMatcher(
            database_url=self.database_url,
            api_key=self.openai_api_key,
            log_level="INFO"
        )

    def demo_single_matching(self):
        """Demonstrate single company matching."""
        logger.info("Testing single company matching...")
        
        test_companies = [
            "Apple Inc",
            "Microsoft Corporation", 
            "Tesla",
            "Amazon",
            "Invalid Company XYZ"
        ]
        
        for company in test_companies:
            result = self.matcher.match(company)
            
            if result["success"]:
                logger.info(
                    "SUCCESS: '%s' matched to '%s' (score: %.1f%%) in %.3fs",
                    company,
                    result["predicted_ticker"] or "No ticker",
                    result["name_match_score"],
                    result["api_latency"]
                )
            else:
                logger.warning(
                    "FAILED: '%s' - %s (%.3fs)",
                    company,
                    result["message"],
                    result["api_latency"]
                )

    def demo_batch_matching(self):
        """Demonstrate batch matching capabilities."""
        logger.info("Testing batch matching...")
        
        companies = ["Apple Inc", "Microsoft Corporation", "Tesla"]
        batch_results = self.matcher.batch_match(companies)
        
        for i, result in enumerate(batch_results):
            company = companies[i]
            if result["success"]:
                logger.info(
                    "Batch result %d: '%s' -> '%s'",
                    i + 1,
                    company,
                    result["predicted_ticker"] or "No ticker"
                )

    def demo_health_and_stats(self):
        """Demonstrate health checking and statistics."""
        # Health check
        health = self.matcher.health_check()
        logger.info("Health Status: %s", health["status"])
        logger.info("Database Records: %d", health["checks"]["database"].get("records_count", 0))
        
        # System stats
        stats = self.matcher.get_stats()
        logger.info("Total Companies in Database: %d", stats.get("total_companies", 0))

    def run_full_demo(self):
        """Run complete demonstration of all features."""
        logger.info("Starting ticker matching service demonstration...")
        
        self.demo_single_matching()
        self.demo_batch_matching()
        self.demo_health_and_stats()
        
        logger.info("Demo completed successfully!")


def run_ticker_demo(database_url: str, openai_api_key: str = None):
    """
    Run ticker matching demonstration with provided configuration.
    
    Args:
        database_url: PostgreSQL database connection URL (required)
        openai_api_key: OpenAI API key for fallback matching (optional)
    """
    if not database_url:
        logger.error("database_url parameter is required")
        return
    
    try:
        # Proper dependency injection - configuration passed explicitly
        demo_service = TickerMatchingExample(
            database_url=database_url,
            openai_api_key=openai_api_key
        )
        
        # Run the demonstration
        demo_service.run_full_demo()
        
    except Exception as e:
        logger.error("Demo failed: %s", e)


# Note: No main() function with os.environ usage  
# Configuration must be passed from app_fastapi.py or other entry points
# Example usage:
#   from src.examples.library_usage_example import run_ticker_demo
#   run_ticker_demo(DATABASE_URL, OPENAI_API_KEY)
