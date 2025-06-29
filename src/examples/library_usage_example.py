"""
Example of using the ticker matching library in a library-first approach.

This demonstrates how engineering teams should integrate the data science
functionality into their Flask/Django applications.

The FastAPI service can be run directly with:
    python src/api/app_fastapi.py
"""

import os
from src.api.ticker_matcher import TickerMatcher


def main():
    """Example of library-first usage pattern."""

    # Configuration must be passed explicitly - no os.environ in library code
    database_url = os.environ.get("DATABASE_URL")
    openai_api_key = os.environ.get("OPENAI_API_KEY")  # Optional

    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required")

    # Initialize the ticker matcher with explicit configuration
    matcher = TickerMatcher(
        database_url=database_url,
        api_key=openai_api_key,  # Can be None for basic matching
        log_level="INFO",
    )

    # Test the matcher
    print("🔍 Testing company matching...")

    test_companies = ["Apple Inc", "Microsoft Corporation", "Tesla", "Amazon.com Inc"]

    for company in test_companies:
        result = matcher.match(company)

        if result["success"]:
            print(
                f"✅ {company} → {result['predicted_ticker']} (score: {result['name_match_score']:.2f})"
            )
        else:
            print(f"❌ {company} → Failed: {result.get('message', 'Unknown error')}")

    # Test health check
    health = matcher.health_check()
    print(f"\n🏥 Health Status: {health['status']}")
    print(
        f"📊 Database Records: {health['checks']['database'].get('records_count', 0)}"
    )

    # Test batch matching
    print(f"\n📦 Batch matching test...")
    batch_results = matcher.batch_match(["Apple", "Google"])
    for result in batch_results:
        company = result.get("input_name", "Unknown")
        ticker = result.get("predicted_ticker", "None")
        print(f"   {company} → {ticker}")


def flask_integration_example():
    """
    Example of how to integrate into a Flask application.
    This would typically be in your Flask app's initialization.
    """
    from flask import Flask

    app = Flask(__name__)

    # Get configuration from environment (allowed in Flask app layer)
    database_url = os.environ.get("DATABASE_URL")
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    if not database_url:
        raise ValueError("DATABASE_URL is required")

    # Initialize the matcher as a singleton
    app.ticker_matcher = TickerMatcher(
        database_url=database_url, api_key=openai_api_key
    )

    @app.route("/match/<company_name>")
    def match_company(company_name):
        """Flask endpoint using the library."""
        result = app.ticker_matcher.match(company_name)
        return result

    return app


if __name__ == "__main__":
    main()
