"""Service responsible only for suffix removal."""

from src.config.settings import settings


class SuffixRemoverService:
    """Service responsible only for suffix removal."""

    def remove_company_suffixes(self, text: str) -> str:
        """
        Remove common company suffixes from text.

        Args:
            text: Text to process

        Returns:
            Text with company suffixes removed
        """
        for suffix in settings.COMPANY_SUFFIXES:
            if text.endswith(suffix):
                text = text[: -len(suffix)]
        return text
