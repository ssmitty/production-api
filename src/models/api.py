"""Pydantic models for FastAPI request/response schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field


class CompanyMatchRequest(BaseModel):
    """Request model for company matching."""

    name: str = Field(..., description="Company name to match", min_length=1)


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    version: str = Field(..., description="API version")


class TopMatch(BaseModel):
    """Model for individual top match results."""

    company_name: str = Field(..., description="Matched company name")
    ticker: str = Field(..., description="Company ticker symbol")
    score: float = Field(..., description="Match confidence score")


class CompanyMatchResponse(BaseModel):
    """Response model for company matching."""

    input_name: str = Field(..., description="Original input company name")
    matched_name: Optional[str] = Field(None, description="Best matched company name")
    predicted_ticker: Optional[str] = Field(None, description="Predicted ticker symbol")
    all_possible_tickers: List[str] = Field(
        default_factory=list, description="All possible ticker matches"
    )
    name_match_score: float = Field(..., description="Confidence score of the match")
    message: Optional[str] = Field(None, description="Status or error message")
    top_matches: List[TopMatch] = Field(
        default_factory=list, description="Top matching results"
    )
    api_latency: float = Field(..., description="API response time in seconds")
    version: str = Field(..., description="API version")


class UpdateTickersResponse(BaseModel):
    """Response model for ticker updates."""

    message: str = Field(..., description="Update status message")
    status: str = Field(..., description="Update status")
    version: str = Field(..., description="API version")


class LatestTickersResponse(BaseModel):
    """Response model for latest tickers timestamp."""

    last_updated: str = Field(..., description="Last update timestamp")
    timezone: str = Field(..., description="Timezone of the timestamp")
    version: str = Field(..., description="API version")


class TimezonesResponse(BaseModel):
    """Response model for available timezones."""

    timezones: List[str] = Field(
        ..., description="List of available timezone identifiers"
    )
    version: str = Field(..., description="API version")


class HealthCheckResponse(BaseModel):
    """Response model for health check."""

    status: str = Field(..., description="Health status")
    database: str = Field(..., description="Database connection status")
    openai_service: str = Field(..., description="OpenAI service availability")
    version: str = Field(..., description="API version")
    error: Optional[str] = Field(None, description="Error details if any")
