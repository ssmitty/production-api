"""Service for OpenAI client initialization."""

from typing import Optional
from openai import OpenAI
import httpx
from src.config.settings import settings


class OpenAIClientService:
    """Service responsible only for initializing OpenAI client."""

    def __init__(self, api_key: str):
        """
        Initialize the OpenAI client service.

        Args:
            api_key: OpenAI API key (required)
        """
        if not api_key:
            raise ValueError("OpenAI API key is required")

        self.api_key = api_key

        self.client = OpenAI(
            api_key=self.api_key,
            http_client=httpx.Client(proxies={}),  # Explicitly disable proxies
        )

    def get_client(self) -> OpenAI:
        """
        Get the initialized OpenAI client.

        Returns:
            OpenAI client instance
        """
        return self.client
