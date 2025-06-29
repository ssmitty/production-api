"""Service responsible only for ETF keyword checking."""

import re
import pandas as pd
from src.config.settings import settings


class ETFKeywordCheckerService:
    """Service responsible only for ETF keyword checking."""

    def check_etf_keywords(self, company_name: str) -> bool:
        """
        Check if company name contains ETF keywords.

        Args:
            company_name: Company name to check

        Returns:
            True if ETF keywords are found, False otherwise
        """
        if not company_name or pd.isna(company_name):
            return False

        name = str(company_name)
        etf_pattern = "|".join(settings.ETF_KEYWORDS)
        return bool(re.search(etf_pattern, name.lower(), re.IGNORECASE))
