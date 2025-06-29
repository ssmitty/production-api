"""Text extraction utility function."""


def extract_company_and_ticker(text: str) -> tuple[str, str]:
    """
    Extract company name and ticker from formatted text.

    Args:
        text: Text containing company name and optionally ticker

    Returns:
        Tuple of (company_name, ticker)
    """
    text = text.strip()

    # Remove common prefixes that might be added by AI responses
    prefixes_to_remove = [
        "Legal Company Name: ",
        "Best match: ",
        "Company: ",
        "Match: ",
    ]

    for prefix in prefixes_to_remove:
        if text.startswith(prefix):
            text = text[len(prefix) :].strip()
            break

    # Extract company name and ticker if in format "Company Name (Ticker: SYMBOL)"
    if " (Ticker:" in text and text.endswith(")"):
        parts = text.split(" (Ticker:")
        company_name = parts[0].strip()
        ticker = parts[1].replace(")", "").strip()
        return company_name, ticker
    else:
        # No ticker format, just company name
        return text.strip(), None
