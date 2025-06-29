"""Service for processing OpenAI responses."""

from typing import List, Dict, Optional, Tuple
from src.utils.text_extractor import extract_company_and_ticker


class OpenAIResponseProcessorService:
    """Service responsible only for processing OpenAI responses."""

    def process_matching_response(
        self, answer: str, candidates: List[Dict]
    ) -> Tuple[str, Optional[Dict]]:
        """
        Process OpenAI response and find matching candidate.

        Args:
            answer: OpenAI response
            candidates: List of candidate companies

        Returns:
            Tuple of (answer, selected_candidate)
        """
        # Extract company name and ticker from response
        openai_company_name, openai_ticker = extract_company_and_ticker(answer)

        # First try to find exact match in candidates
        selected = next(
            (
                c
                for c in candidates
                if extract_company_and_ticker(c["company_name"])[0]
                == openai_company_name
            ),
            None,
        )

        # If no exact match found but answer is not 'None',
        # OpenAI likely provided a legal company name with ticker
        if selected is None and answer.lower() != "none":
            selected = {
                "company_name": openai_company_name,
                "ticker": openai_ticker,
                "score": 95.0,  # High confidence for OpenAI brand name recognition
            }

        return answer, selected
