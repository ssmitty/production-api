"""Service for managing database metadata."""

import logging
import pandas as pd
import pytz
from typing import Dict, Any
from sqlalchemy import create_engine, text


class MetadataService:
    """Service responsible only for managing database metadata."""

    def __init__(self, database_url: str):
        """
        Initialize the metadata service.

        Args:
            database_url: Database connection URL
        """
        self.database_url = database_url

    def update_last_updated(self) -> None:
        """Update the last updated timestamp in metadata table."""
        try:
            engine = create_engine(self.database_url)
            with engine.connect() as connection:
                # Ensure metadata table exists
                connection.execute(
                    text(
                        "CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT)"
                    )
                )

                # Update timestamp
                timestamp = pd.Timestamp.now(tz="UTC").isoformat()
                connection.execute(
                    text(
                        "INSERT INTO metadata (key, value) VALUES ('last_updated', :timestamp) "
                        "ON CONFLICT (key) DO UPDATE SET value = :timestamp"
                    ),
                    {"timestamp": timestamp},
                )

                connection.commit()

        except Exception as e:
            logging.error("Error updating last_updated timestamp: %s", e)
            raise

    def get_last_update_time(self, timezone: str = "UTC") -> Dict[str, Any]:
        """
        Get the last update time from the database.

        Args:
            timezone: Target timezone for the result

        Returns:
            Dictionary with last_updated time and status information
        """
        try:
            engine = create_engine(self.database_url)
            with engine.connect() as connection:
                result = connection.execute(
                    text("SELECT value FROM metadata WHERE key = 'last_updated'")
                ).scalar_one_or_none()

            if result is None:
                return {
                    "error": "Last update time not found. The update process may not have run yet.",
                    "status": 404,
                }

            # Parse timestamp
            last_updated_utc = pd.to_datetime(result)
            if last_updated_utc.tzinfo is None:
                last_updated_utc = last_updated_utc.tz_localize("UTC")

            # Convert timezone
            try:
                target_tz = pytz.timezone(timezone)
            except pytz.UnknownTimeZoneError:
                return {
                    "error": f"Invalid timezone: {timezone}. See /timezones for options.",
                    "status": 400,
                }

            last_updated_local = last_updated_utc.astimezone(target_tz)

            return {
                "last_updated": last_updated_local.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
                "timezone": timezone,
                "status": 200,
            }

        except Exception as e:
            logging.error("Error getting ticker update time: %s", e)
            return {"error": "An unexpected error occurred", "status": 500}
