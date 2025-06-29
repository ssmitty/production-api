"""Company name cleaning utility using micro-services architecture."""

from typing import Optional

from src.utils.text_processing import (
    TextCaseConverterService,
    AlphanumericCleanerService,
    SuffixRemoverService,
    WhitespaceNormalizerService,
)


class CompanyNameProcessor:
    """Property-based company name processor using micro-services for chaining operations."""

    def __init__(
        self,
        name: str,
        case_converter: Optional[TextCaseConverterService] = None,
        alphanumeric_cleaner: Optional[AlphanumericCleanerService] = None,
        suffix_remover: Optional[SuffixRemoverService] = None,
        whitespace_normalizer: Optional[WhitespaceNormalizerService] = None,
    ):
        """
        Initialize with a company name and micro-services.

        Args:
            name: Company name to process
            case_converter: Service for case conversion
            alphanumeric_cleaner: Service for alphanumeric cleaning
            suffix_remover: Service for suffix removal
            whitespace_normalizer: Service for whitespace normalization
        """
        self._name = name if isinstance(name, str) else str(name)

        # Initialize micro-services
        self._case_converter = case_converter or TextCaseConverterService()
        self._alphanumeric_cleaner = (
            alphanumeric_cleaner or AlphanumericCleanerService()
        )
        self._suffix_remover = suffix_remover or SuffixRemoverService()
        self._whitespace_normalizer = (
            whitespace_normalizer or WhitespaceNormalizerService()
        )

    @property
    def lowercased(self) -> "CompanyNameProcessor":
        """Convert to lowercase using micro-service."""
        converted = self._case_converter.convert_to_lowercase(self._name)
        return CompanyNameProcessor(
            converted,
            self._case_converter,
            self._alphanumeric_cleaner,
            self._suffix_remover,
            self._whitespace_normalizer,
        )

    @property
    def alphanumeric_only(self) -> "CompanyNameProcessor":
        """Remove all non-alphanumeric except spaces using micro-service."""
        cleaned = self._alphanumeric_cleaner.clean_to_alphanumeric(self._name)
        return CompanyNameProcessor(
            cleaned,
            self._case_converter,
            self._alphanumeric_cleaner,
            self._suffix_remover,
            self._whitespace_normalizer,
        )

    @property
    def without_suffixes(self) -> "CompanyNameProcessor":
        """Remove common company suffixes using micro-service."""
        cleaned = self._suffix_remover.remove_company_suffixes(self._name)
        return CompanyNameProcessor(
            cleaned,
            self._case_converter,
            self._alphanumeric_cleaner,
            self._suffix_remover,
            self._whitespace_normalizer,
        )

    @property
    def normalized_whitespace(self) -> "CompanyNameProcessor":
        """Normalize whitespace using micro-service."""
        normalized = self._whitespace_normalizer.normalize_whitespace(self._name)
        return CompanyNameProcessor(
            normalized,
            self._case_converter,
            self._alphanumeric_cleaner,
            self._suffix_remover,
            self._whitespace_normalizer,
        )

    @property
    def value(self) -> str:
        """Get the final processed value."""
        return self._name

    def __str__(self) -> str:
        """String representation."""
        return self._name


def preprocess_company_name(name: str) -> str:
    """
    Remove common company suffixes and non-alphanumeric chars for better matching.

    Args:
        name: Company name to preprocess

    Returns:
        Preprocessed company name
    """
    if not isinstance(name, str):
        return name

    # Property-style chaining approach using micro-services
    processor = CompanyNameProcessor(name)
    return (
        processor.lowercased.alphanumeric_only.without_suffixes.normalized_whitespace.value
    )


def remove_suffix(text: str, suffix: str) -> str:
    """
    Property-style suffix removal function.

    Args:
        text: Text to process
        suffix: Suffix to remove

    Returns:
        Text with suffix removed if it existed
    """
    if text.endswith(suffix):
        return text[: -len(suffix)]
    return text
