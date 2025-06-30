"""Simple application configuration settings."""

from typing import Optional


class Settings:
    """Simple application settings - only what's actually used."""

    # API Configuration - Only thing actually used by FastAPI
    APP_VERSION: str = "1.3.0"

    # Static configurations that don't need environment loading
    ALPHA_VANTAGE_BASE_URL: str = "https://www.alphavantage.co"
    HOST: str = "0.0.0.0"
    DEBUG: bool = True

    # Configuration properties that must be passed through constructors
    # These are None by default and should be injected via constructor parameters
    OPENAI_API_KEY: Optional[str] = None
    ALPHA_VANTAGE_API_KEY: Optional[str] = None
    DATABASE_URL: Optional[str] = None

    # Matching Configuration
    FUZZY_MATCH_THRESHOLD: int = 90
    ML_NEIGHBORS_COUNT: int = 5
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_MAX_TOKENS: int = 20
    OPENAI_TEMPERATURE: float = 0

    # ETF Filtering Keywords
    ETF_KEYWORDS: list = [
        "etf",
        "fund",
        "trust",
        "index",
        "spdr",
        "ishares",
        "vanguard",
        "invesco",
        "direxion",
        "proshares",
        "wisdomtree",
        "first trust",
        "global x",
        "pacer",
        "vaneck",
        "blackrock",
        "amplify",
        "ark",
        "bull",
        "bear",
        "leveraged",
        "inverse",
        "daily",
        "2x",
        "3x",
        "ultra",
        "short",
        "long",
    ]

    # Company Name Suffixes for Preprocessing
    COMPANY_SUFFIXES: list = [
        " inc",
        " corporation",
        " corp",
        " ltd",
        " llc",
        " co",
        " - common stock",
        "- common stock",
        " common stock",
        " incorporated",
        " plc",
        " group",
        " holdings",
        " company",
        " companies",
        " lp",
        " ag",
        " sa",
        " nv",
        " spa",
        " srl",
        " limited",
        " the",
        " and",
        " of",
        " dba",
        " llp",
        " pty",
        " s p a",
        " s a",
    ]


# Global settings instance
settings = Settings()
