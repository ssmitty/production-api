"""Service for finding fuzzy matches."""

from typing import List, Tuple
from rapidfuzz import process
from src.config.settings import settings


class FuzzyMatchFinderService:
    """Service responsible only for finding fuzzy matches."""

    def find_fuzzy_matches(
        self, name_processed: str, title_list: List[str]
    ) -> List[Tuple]:
        """
        Find fuzzy matches for a preprocessed company name.

        Args:
            name_processed: Preprocessed company name
            title_list: List of preprocessed company titles

        Returns:
            List of fuzzy match tuples
        """
        matches = process.extract(name_processed, title_list, limit=10)
        return matches

    def filter_strong_matches(self, fuzzy_matches: List) -> List[Tuple]:
        """
        Filter fuzzy matches that meet the threshold requirement.

        Args:
            fuzzy_matches: List of fuzzy match results

        Returns:
            List of strong matches as (company_name, score) tuples
        """
        strong_matches = []
        for match in fuzzy_matches:
            if len(match) == 3:
                company, score, _ = match
            else:
                company, score = match

            if score >= settings.FUZZY_MATCH_THRESHOLD:
                strong_matches.append((company, round(score, 1)))

        return strong_matches
