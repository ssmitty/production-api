"""
Consolidated FastAPI application for ticker matching service.

This file contains everything needed to run the ticker matching API:
- Environment variable loading from .env.secrets
- FastAPI app configuration and routes
- Built-in server runner
- All dependencies and services

Usage:
    python app_fastapi.py              # Runs the server
    python -m uvicorn app_fastapi:app  # Alternative way to run
"""

import os
import sys
import logging
import asyncio
import pytz
import uvicorn
from typing import Optional, Dict, Any

# Add project root to Python path for proper imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from fastapi import FastAPI, HTTPException, status, Form, Query, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.config.settings import settings
from src.models.api import (
    CompanyMatchRequest,
    CompanyMatchResponse,
    UpdateTickersResponse,
    LatestTickersResponse,
    TimezonesResponse,
    HealthCheckResponse,
    ErrorResponse,
)
from src.core.services.company_matcher_service import CompanyMatcherService
from src.core.services.ticker_updater_service import TickerUpdaterService
from src.database.repositories import (
    TickerDataFrameLoaderService,
    TickerDataFrameSaverService,
    MetadataService,
    DatabaseHealthService,
)
from src.core.services.openai_service import OpenAIService

# Load environment variables first
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Environment variables - accessed directly in main app
DATABASE_URL = os.environ.get("DATABASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")
PORT = int(os.environ.get("PORT", 8000))
HOST = os.environ.get("HOST", "0.0.0.0")
DEBUG = os.environ.get("DEBUG", "true").lower() == "true"

# Validate required environment variables
if not DATABASE_URL:
    logger.error("❌ DATABASE_URL environment variable is required")
    sys.exit(1)

if not ALPHA_VANTAGE_API_KEY:
    logger.error("❌ ALPHA_VANTAGE_API_KEY environment variable is required")
    sys.exit(1)

# Create FastAPI app
app = FastAPI(
    title="Company Ticker Matching API",
    description="API for matching company names to stock tickers",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services with direct dependency injection
dataframe_loader = TickerDataFrameLoaderService(DATABASE_URL)
dataframe_saver = TickerDataFrameSaverService(DATABASE_URL)
metadata_service = MetadataService(DATABASE_URL)
health_service = DatabaseHealthService(DATABASE_URL)

# Initialize OpenAI service (optional)
openai_service = None
if OPENAI_API_KEY:
    try:
        openai_service = OpenAIService(OPENAI_API_KEY)
        logger.info("✅ OpenAI service initialized successfully")
    except Exception as e:
        logger.warning("⚠️ Failed to initialize OpenAI service: %s", e)

# Initialize main services
company_matcher = CompanyMatcherService(
    dataframe_loader=dataframe_loader, openai_service=openai_service
)
ticker_updater = TickerUpdaterService(api_key=ALPHA_VANTAGE_API_KEY)

logger.info("✅ All services initialized successfully")


@app.get("/")
def root():
    """Redirect to API documentation."""
    return RedirectResponse(url="/docs")


@app.get("/home", response_class=HTMLResponse)
def home_form():
    """Home Page: Renders a simple HTML form for company name input."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Company Ticker Matching</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 50px; }
            .form-container { max-width: 500px; margin: auto; }
            .form-group { margin: 20px 0; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input[type="text"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
            input[type="submit"] { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            input[type="submit"]:hover { background-color: #0056b3; }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h1>Company Ticker Matching</h1>
            <form method="post" action="/match">
                <div class="form-group">
                    <label for="name">Company Name:</label>
                    <input type="text" id="name" name="name" placeholder="Enter company name" required>
                </div>
                <div class="form-group">
                    <input type="submit" value="Find Ticker">
                </div>
            </form>
        </div>
    </body>
    </html>
    """


@app.post("/match", response_model=CompanyMatchResponse)
async def match_company_form(name: str = Form(...)):
    """
    Company Matcher API Endpoint (Form submission)
    Match a company name to its stock ticker using form data.
    """
    try:
        if not name or not name.strip():
            raise HTTPException(status_code=400, detail="No company name provided")

        # Perform matching using the service
        result = company_matcher.match_company(name.strip())

        # Check if matching was successful
        if result.message == "No ticker data available":
            logger.error("Ticker data is not available from the database")
            raise HTTPException(
                status_code=503,
                detail="Ticker data is currently unavailable. Please try again later.",
            )

        # Log API latency for monitoring
        logger.info("API Latency for '%s': %.4f seconds", name, result.api_latency)

        # Format response
        top_matches = []
        if result.top_matches:
            for match in result.top_matches[:5]:  # Limit to top 5
                if isinstance(match, dict):
                    # Debug: Log the actual match data structure
                    logger.info("🔍 Match data structure: %s", match)
                    
                    # Use the correct key name and ensure score is properly formatted
                    score = match.get("name_match_score", match.get("score", 0))
                    logger.info("🔍 Extracted score: %s from name_match_score: %s, score: %s", 
                                score, match.get("name_match_score"), match.get("score"))
                    
                    top_matches.append(
                        {
                            "company_name": match.get("company_name", ""),
                            "ticker": match.get("ticker", ""),
                            "score": round(score, 1) if isinstance(score, (int, float)) else 0,
                        }
                    )

        return CompanyMatchResponse(
            input_name=name,
            matched_name=result.matched_name,
            predicted_ticker=result.predicted_ticker,
            all_possible_tickers=result.all_possible_tickers or [],
            name_match_score=result.name_match_score,
            message=result.message,
            top_matches=top_matches,
            api_latency=result.api_latency,
            version=settings.APP_VERSION,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("API error in /match: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/match", response_model=CompanyMatchResponse)
async def match_company_api(request: CompanyMatchRequest):
    """
    Company Matcher API Endpoint (JSON)
    Match a company name to its stock ticker using JSON payload.
    """
    try:
        if not request.company_name or not request.company_name.strip():
            raise HTTPException(status_code=400, detail="No company name provided")

        # Perform matching using the service
        result = company_matcher.match_company(request.company_name.strip())

        # Check if matching was successful
        if result.message == "No ticker data available":
            logger.error("Ticker data is not available from the database")
            raise HTTPException(
                status_code=503,
                detail="Ticker data is currently unavailable. Please try again later.",
            )

        # Log API latency for monitoring
        logger.info(
            "API Latency for '%s': %.4f seconds",
            request.company_name,
            result.api_latency,
        )

        # Format response
        top_matches = []
        if result.top_matches:
            for match in result.top_matches[:5]:  # Limit to top 5
                if isinstance(match, dict):
                    # Debug: Log the actual match data structure
                    logger.info("🔍 Match data structure: %s", match)
                    
                    # Use the correct key name and ensure score is properly formatted
                    score = match.get("name_match_score", match.get("score", 0))
                    logger.info("🔍 Extracted score: %s from name_match_score: %s, score: %s", 
                                score, match.get("name_match_score"), match.get("score"))
                    
                    top_matches.append(
                        {
                            "company_name": match.get("company_name", ""),
                            "ticker": match.get("ticker", ""),
                            "score": round(score, 1) if isinstance(score, (int, float)) else 0,
                        }
                    )

        return CompanyMatchResponse(
            input_name=request.company_name,
            matched_name=result.matched_name,
            predicted_ticker=result.predicted_ticker,
            all_possible_tickers=result.all_possible_tickers or [],
            name_match_score=result.name_match_score,
            message=result.message,
            top_matches=top_matches,
            api_latency=result.api_latency,
            version=settings.APP_VERSION,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("API error in /api/match: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/update-tickers", response_model=UpdateTickersResponse)
async def update_tickers():
    """
    Update Tickers Endpoint
    Fetch and save latest ticker data from Alpha Vantage API.
    """
    try:
        # Fetch ticker data using the service
        tickers_df = await ticker_updater.fetch_ticker_dataframe()

        if tickers_df.empty:
            raise HTTPException(
                status_code=503, detail="Failed to fetch ticker data from API"
            )

        # Save to database
        dataframe_saver.save_tickers_dataframe(tickers_df)

        # Update metadata
        metadata_service.update_last_updated()

        return UpdateTickersResponse(
            status="success",
            message=f"Successfully updated {len(tickers_df)} tickers",
            records_updated=len(tickers_df),
            version=settings.APP_VERSION,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error in /update-tickers: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/latest-tickers", response_model=LatestTickersResponse)
async def latest_tickers(
    tz: str = Query("UTC", description="Timezone (e.g., 'America/New_York')")
):
    """
    Latest Tickers Endpoint
    Get the timestamp of the last ticker data update.
    """
    try:
        # Use metadata service to get last update time
        result = metadata_service.get_last_update_time(tz)

        if result["status"] != 200:
            raise HTTPException(
                status_code=result["status"],
                detail=result.get("error", "Unknown error"),
            )

        return LatestTickersResponse(
            last_updated=result["last_updated"],
            timezone=result["timezone"],
            message="Latest ticker data timestamp retrieved successfully",
            version=settings.APP_VERSION,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error in /latest-tickers: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/timezones", response_model=TimezonesResponse)
async def list_timezones():
    """
    Timezones Endpoint
    List all available timezones for the latest-tickers endpoint.
    """
    try:
        common_timezones = [
            "UTC",
            "America/New_York",
            "America/Chicago",
            "America/Denver",
            "America/Los_Angeles",
            "Europe/London",
            "Europe/Paris",
            "Asia/Tokyo",
            "Asia/Shanghai",
            "Australia/Sydney",
        ]

        return TimezonesResponse(
            timezones=common_timezones,
            message="Available timezones retrieved successfully",
            version=settings.APP_VERSION,
        )

    except Exception as e:
        logger.exception("Error in /timezones: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health Check Endpoint
    Basic health check for load balancer - just confirms app is running.
    """
    try:
        # Basic health check for EB load balancer - always return healthy if app is running
        return HealthCheckResponse(
            status="healthy",
            database="not_checked",  # Don't check DB for basic health check
            openai_service="not_checked",  # Don't check OpenAI for basic health check
            version=settings.APP_VERSION,
        )

    except Exception as e:
        logger.exception("Health check error: %s", e)
        raise HTTPException(
            status_code=503,
            detail=HealthCheckResponse(
                status="unhealthy",
                database="error",
                openai_service="error",
                version=settings.APP_VERSION,
                error=str(e),
            ).dict(),
        )


@app.get("/health/detailed", response_model=HealthCheckResponse)
async def detailed_health_check():
    """
    Detailed Health Check Endpoint
    Check the health of the application and its dependencies.
    """
    try:
        # Check database health using service
        is_healthy = health_service.health_check()

        # Check OpenAI service availability
        openai_available = openai_service.is_available() if openai_service else False

        if is_healthy:
            return HealthCheckResponse(
                status="healthy",
                database="connected",
                openai_service="available" if openai_available else "unavailable",
                version=settings.APP_VERSION,
            )
        else:
            raise HTTPException(
                status_code=503,
                detail=HealthCheckResponse(
                    status="unhealthy",
                    database="disconnected",
                    openai_service="unavailable",
                    version=settings.APP_VERSION,
                ).dict(),
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Detailed health check error: %s", e)
        raise HTTPException(
            status_code=503,
            detail=HealthCheckResponse(
                status="unhealthy",
                database="error",
                openai_service="error",
                version=settings.APP_VERSION,
                error=str(e),
            ).dict(),
        )


def run_server():
    """Run the FastAPI server with uvicorn."""
    logger.info("🚀 Starting FastAPI ticker matching server...")
    logger.info(f"📍 Server will be available at: http://{HOST}:{PORT}")
    logger.info(f"📚 API Documentation at: http://{HOST}:{PORT}/docs")
    logger.info(f"🔄 Debug mode: {DEBUG}")
    logger.info("🔥 Press Ctrl+C to stop the server")
    logger.info("-" * 50)

    uvicorn.run(
        "src.api.app_fastapi:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info",
        access_log=True,
    )


if __name__ == "__main__":
    run_server()
