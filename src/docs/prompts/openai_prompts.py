"""OpenAI prompts for company matching."""


class OpenAIPrompts:
    """Class responsible only for storing OpenAI prompts."""

    @staticmethod
    def get_company_matching_prompt(company_name: str, candidates: list) -> str:
        """
        Get the prompt for company name matching with brand name recognition.

        Args:
            company_name: The input company name to match
            candidates: List of candidate companies

        Returns:
            Formatted prompt string for OpenAI
        """
        candidates_text = ""
        for i, candidate in enumerate(candidates, 1):
            candidates_text += (
                f"{i}. {candidate['company_name']} (Ticker: {candidate['ticker']})\n"
            )

        prompt = f"""
You are an expert at matching company names and understanding the difference between brand names and legal company names.

TASK: Given the input company name, find the best match from the candidate list OR identify the correct legal company name and ticker if the input is a well-known brand/common name.

RULES:
1. FIRST: Check if the input directly matches any candidate (even with misspellings)
2. SECOND: If no direct match, consider if the input is a well-known brand name for a public company
3. Examples of brand name mappings with tickers:
   - "Google" → "Alphabet Inc. (Ticker: GOOGL)"
   - "Facebook" → "Meta Platforms Inc. (Ticker: META)"
   - "Tesla" → "Tesla Inc. (Ticker: TSLA)"
   - "Amazon" → "Amazon.com Inc. (Ticker: AMZN)"
   - "Apple" → "Apple Inc. (Ticker: AAPL)"
   - "AMD" → "Advanced Micro Devices Inc. (Ticker: AMD)"
   - "IBM" → "International Business Machines Corporation (Ticker: IBM)"

Input company name: {company_name}

Candidates:
{candidates_text}

RESPONSE FORMAT:
- If you find a match in the candidates: Reply with the exact company name from the list above
- If the input is a well-known brand name but not in candidates: Reply with the actual legal company name and ticker in this format: "Company Name (Ticker: SYMBOL)"
- If you're unsure or the company is not well-known: Reply with 'None'

Examples of correct responses:
- For "Google": "Alphabet Inc. (Ticker: GOOGL)"
- For "Facebook": "Meta Platforms Inc. (Ticker: META)"

Best match or legal company name with ticker:"""

        return prompt
