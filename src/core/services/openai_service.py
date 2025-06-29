"""OpenAI service for company name matching fallback."""

from typing import List, Dict, Optional, Tuple
from src.core.services.ai.openai_client_service import OpenAIClientService
from src.core.services.ai.openai_request_service import OpenAIRequestService
from src.core.services.ai.openai_response_processor_service import (
    OpenAIResponseProcessorService,
)
from src.core.services.ai.openai_availability_checker_service import (
    OpenAIAvailabilityCheckerService,
)


class OpenAIService:
    """Service for OpenAI-based company name matching."""

    def __init__(self, api_key: str):
        """
        Initialize the OpenAI service.

        Args:
            api_key: OpenAI API key (required)
        """
        # Initialize micro-services
        self.client_service = OpenAIClientService(api_key)
        self.request_service = OpenAIRequestService(self.client_service.get_client())
        self.response_processor = OpenAIResponseProcessorService()
        self.availability_checker = OpenAIAvailabilityCheckerService(
            self.client_service.api_key
        )

    def find_best_match(
        self, company_name: str, candidates: List[Dict]
    ) -> Tuple[str, Optional[Dict]]:
        """
        Use OpenAI to select the best match from a list of candidates.
        Enhanced to handle brand names vs legal company names.

        Args:
            company_name: Company name to match
            candidates: List of candidate dictionaries with company_name and ticker

        Returns:
            Tuple of (openai_response, selected_candidate)
        """
        # Make request to OpenAI
        answer = self.request_service.make_matching_request(company_name, candidates)

        # Process the response
        return self.response_processor.process_matching_response(answer, candidates)

    def is_available(self) -> bool:
        """
        Check if OpenAI service is available (API key is set).

        Returns:
            True if service is available, False otherwise
        """
        return self.availability_checker.is_available()
