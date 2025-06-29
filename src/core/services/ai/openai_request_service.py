"""Service for making OpenAI API requests."""

import logging
from typing import List, Dict
from openai import OpenAI
from src.config.settings import settings
from src.docs.prompts.openai_prompts import OpenAIPrompts


class OpenAIRequestService:
    """Service responsible only for making OpenAI API requests."""

    def __init__(self, client: OpenAI):
        """
        Initialize the OpenAI request service.

        Args:
            client: Initialized OpenAI client
        """
        self.client = client

    def make_matching_request(self, company_name: str, candidates: List[Dict]) -> str:
        """
        Make a request to OpenAI for company name matching.

        Args:
            company_name: Company name to match
            candidates: List of candidate dictionaries with company_name and ticker

        Returns:
            OpenAI response string
        """
        prompt = OpenAIPrompts.get_company_matching_prompt(company_name, candidates)

        # Log the matching attempt
        logging.info("[OpenAI Fallback] Input Name: %s", company_name)
        logging.info(
            "[OpenAI Fallback] Candidates: %s", [c["company_name"] for c in candidates]
        )
        logging.info("[OpenAI Fallback] Prompt:\n%s", prompt)

        # Get OpenAI response
        response = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=settings.OPENAI_MAX_TOKENS,
            temperature=settings.OPENAI_TEMPERATURE,
        )

        answer = response.choices[0].message.content.strip()
        logging.info("[OpenAI Fallback] OpenAI returned: %s", answer)

        return answer
