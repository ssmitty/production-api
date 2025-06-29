"""Service for database health checks."""

import logging
from sqlalchemy import create_engine, text


class DatabaseHealthService:
    """Service responsible only for database health checks."""

    def __init__(self, database_url: str):
        """
        Initialize the database health service.

        Args:
            database_url: Database connection URL
        """
        self.database_url = database_url

    def health_check(self) -> bool:
        """
        Check if database connection is healthy.

        Returns:
            True if connection is healthy, False otherwise
        """
        try:
            engine = create_engine(self.database_url)
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logging.error("Database health check failed: %s", e)
            return False
