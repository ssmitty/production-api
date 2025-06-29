"""Service responsible only for fund type classification."""

import re
import pandas as pd


class FundTypeClassifierService:
    """Service responsible only for fund type classification."""

    def classify_as_fund(self, company_name: str) -> bool:
        """
        Check if company name indicates it's a fund.

        Args:
            company_name: Company name to check

        Returns:
            True if it's classified as a fund, False otherwise
        """
        if not company_name or pd.isna(company_name):
            return False

        name = str(company_name)
        fund_keywords = ["fund", "etf", "trust", "index"]
        pattern = "|".join(fund_keywords)
        return bool(re.search(pattern, name.lower(), re.IGNORECASE))

    def classify_as_leveraged(self, company_name: str) -> bool:
        """
        Check if company name indicates it's leveraged.

        Args:
            company_name: Company name to check

        Returns:
            True if it's classified as leveraged, False otherwise
        """
        if not company_name or pd.isna(company_name):
            return False

        name = str(company_name)
        leveraged_keywords = ["2x", "3x", "ultra", "leveraged", "bull", "bear"]
        pattern = "|".join(leveraged_keywords)
        return bool(re.search(pattern, name.lower(), re.IGNORECASE))
