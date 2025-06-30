"""Database export utility with proper dependency injection."""

import logging
import pandas as pd
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class DatabaseExportService:
    """Service for exporting database data to CSV files."""

    def __init__(self, database_url: str):
        """
        Initialize the export service with database connection.

        Args:
            database_url: PostgreSQL database connection URL
        """
        if not database_url:
            raise ValueError("database_url is required")

        self.database_url = database_url

    def export_to_csv(self, output_file: str = "tickers_export.csv") -> None:
        """
        Export ticker database to CSV file.

        Args:
            output_file: Name of the output CSV file
        """
        try:
            # Create database connection
            engine = create_engine(self.database_url)

            # Query all tickers
            query = "SELECT * FROM tickers ORDER BY ticker"
            df = pd.read_sql_query(query, engine)

            # Export to CSV
            df.to_csv(output_file, index=False)

            logger.info("Exported %d tickers to %s", len(df), output_file)
            logger.info("Sample data:")
            logger.info("\n%s", df.head().to_string())

        except (ValueError, ConnectionError, RuntimeError) as e:
            logger.error("Error exporting database: %s", e)


def export_database_to_csv(database_url: str, output_file: str = "tickers_export.csv") -> None:
    """
    Export database to CSV with dependency injection.

    Args:
        database_url: PostgreSQL database connection URL (must be provided)
        output_file: Name of the output CSV file
    """
    if not database_url:
        logger.error("database_url parameter is required")
        return

    export_service = DatabaseExportService(database_url)
    export_service.export_to_csv(output_file)


# Note: No main() function with os.environ usage
# Configuration must be passed from app_fastapi.py or other entry points
