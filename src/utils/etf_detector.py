"""ETF detection utility using micro-services architecture."""

import pandas as pd
from typing import List, Optional

from src.utils.etf_detection import ETFKeywordCheckerService, FundTypeClassifierService


class ETFDetector:
    """Property-based ETF detector using micro-services for individual company names."""

    def __init__(
        self,
        company_name: str,
        keyword_checker: Optional[ETFKeywordCheckerService] = None,
        type_classifier: Optional[FundTypeClassifierService] = None,
    ):
        """
        Initialize with a company name and micro-services.

        Args:
            company_name: Company name to analyze
            keyword_checker: Service for ETF keyword checking
            type_classifier: Service for fund type classification
        """
        self._name = str(company_name) if pd.notna(company_name) else ""

        # Initialize micro-services
        self._keyword_checker = keyword_checker or ETFKeywordCheckerService()
        self._type_classifier = type_classifier or FundTypeClassifierService()

    @property
    def is_etf(self) -> bool:
        """Check if the company name indicates it's an ETF using micro-service."""
        return self._keyword_checker.check_etf_keywords(self._name)

    @property
    def is_fund(self) -> bool:
        """Check if the company name indicates it's a fund using micro-service."""
        return self._type_classifier.classify_as_fund(self._name)

    @property
    def is_leveraged(self) -> bool:
        """Check if the company name indicates it's leveraged using micro-service."""
        return self._type_classifier.classify_as_leveraged(self._name)

    @property
    def etf_type(self) -> str:
        """Get the type of ETF if it is one using micro-services."""
        if not self.is_etf:
            return "not_etf"
        elif self.is_leveraged:
            return "leveraged_etf"
        elif self.is_fund:
            return "regular_etf"
        else:
            return "unknown_etf"


def filter_etfs(company_names: List[str]) -> List[bool]:
    """
    Identify ETFs based on company name keywords using micro-services.

    Args:
        company_names: List of company names to filter (may contain NaN values)

    Returns:
        List of boolean values indicating whether each name is an ETF
    """
    return [ETFDetector(name).is_etf for name in company_names]


def detect_etf(company_name: str) -> bool:
    """
    Property-style ETF detection for a single company name using micro-services.

    Args:
        company_name: Company name to check

    Returns:
        True if the name indicates an ETF, False otherwise
    """
    return ETFDetector(company_name).is_etf
