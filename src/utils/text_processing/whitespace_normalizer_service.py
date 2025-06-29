"""Service responsible only for whitespace normalization."""

import re


class WhitespaceNormalizerService:
    """Service responsible only for whitespace normalization."""

    def normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace by collapsing multiple spaces and stripping.

        Args:
            text: Text to normalize

        Returns:
            Text with normalized whitespace
        """
        return re.sub(r"\s+", " ", text).strip()
