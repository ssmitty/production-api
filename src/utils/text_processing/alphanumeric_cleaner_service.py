"""Service responsible only for alphanumeric cleaning."""

import re


class AlphanumericCleanerService:
    """Service responsible only for alphanumeric cleaning."""

    def clean_to_alphanumeric(self, text: str) -> str:
        """
        Remove all non-alphanumeric characters except spaces.

        Args:
            text: Text to clean

        Returns:
            Cleaned text with only alphanumeric characters and spaces
        """
        return re.sub(r"[^a-z0-9 ]", "", text)
