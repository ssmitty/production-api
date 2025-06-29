"""Service responsible only for OpenAI fallback matching."""

import logging
from typing import List, Dict, Tuple, Optional

from src.core.services.openai_service import OpenAIService


class OpenAIFallbackService:
    """Service responsible only for OpenAI fallback matching."""

    def __init__(self, openai_service: OpenAIService):
        """
        Initialize the OpenAI fallback service.

        Args:
            openai_service: OpenAI service for making requests
        """
        self.openai_service = openai_service

    def try_openai_fallback(self, name: str, candidates: List[Dict]) -> Tuple:
        """
        Try using OpenAI fallback for company matching.

        Args:
            name: Company name to match
            candidates: List of candidate companies

        Returns:
            Tuple with match results
        """
        if not self.openai_service:
            return None, None, [], 0, "OpenAI service not available", []

        try:
            openai_result, selected = self.openai_service.find_best_match(
                name, candidates
            )

            if openai_result == "None" or selected is None:
                return None, None, [], 0, "Company is not in public company list", []

            logging.info("OpenAI score: %s", selected["score"])
            return (
                selected["company_name"],
                selected["ticker"],
                [selected["ticker"]],
                selected["score"],
                None,
                [
                    {
                        "Rank": 1,
                        "company_name": selected["company_name"],
                        "ticker": selected["ticker"],
                        "name_match_score": selected["score"],
                    }
                ],
            )
        except Exception as e:
            logging.error("OpenAI fallback failed: %s", e)
            return None, None, [], 0, "OpenAI service error", []
