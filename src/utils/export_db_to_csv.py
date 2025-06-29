"""
Export database tickers to CSV file for inspection.
"""

import os
import pandas as pd
from sqlalchemy import create_engine
import logging


def export_tickers_to_csv():
    """Export tickers table from database to CSV file."""

    # Get database URL from environment
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        return

    try:
        # Connect to database
        engine = create_engine(database_url)

        # Query all tickers
        query = "SELECT ticker, title FROM tickers ORDER BY ticker"
        df = pd.read_sql(query, engine)

        # Export to CSV
        output_file = "database_tickers.csv"
        df.to_csv(output_file, index=False)

        print(f"✅ Exported {len(df)} tickers to {output_file}")
        print(f"📊 Sample data:")
        print(df.head())

    except Exception as e:
        print(f"❌ Error exporting database: {e}")


if __name__ == "__main__":
    export_tickers_to_csv()
