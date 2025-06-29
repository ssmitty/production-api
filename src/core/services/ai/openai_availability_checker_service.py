"""Service for checking OpenAI availability."""

from typing import Optional


class OpenAIAvailabilityCheckerService:
    """Service responsible only for checking OpenAI availability."""

    def __init__(self, api_key: Optional[str]):
        """
        Initialize the availability checker.

        Args:
            api_key: OpenAI API key
        """
        self.api_key = api_key

    def is_available(self) -> bool:
        """
        Check if OpenAI service is available (API key is set).

        Returns:
            True if service is available, False otherwise
        """
        return self.api_key is not None
