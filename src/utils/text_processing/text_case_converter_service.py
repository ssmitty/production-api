"""Service responsible only for text case conversion."""


class TextCaseConverterService:
    """Service responsible only for text case conversion."""

    def convert_to_lowercase(self, text: str) -> str:
        """
        Convert text to lowercase.

        Args:
            text: Text to convert

        Returns:
            Lowercase text
        """
        return text.lower() if isinstance(text, str) else str(text).lower()
