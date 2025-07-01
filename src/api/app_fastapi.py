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
import uvicorn
from fastapi import FastAPI, HTTPException, Form, Query
from fastapi.middleware.cors import CORSMiddleware

# Add project root to Python path for proper imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.config.settings import settings
from src.models.api import (
    CompanyMatchResponse,
    UpdateTickersResponse,
    LatestTickersResponse,
    TimezonesResponse,
    HealthCheckResponse,
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
OPENAI_SERVICE = None
if OPENAI_API_KEY:
    try:
        OPENAI_SERVICE = OpenAIService(OPENAI_API_KEY)
        logger.info("SUCCESS: OpenAI service initialized successfully")
    except Exception as e:
        logger.warning("WARNING: Failed to initialize OpenAI service: %s", e)

# Initialize main services
company_matcher = CompanyMatcherService(
    dataframe_loader=dataframe_loader, openai_service=OPENAI_SERVICE
)
ticker_updater = TickerUpdaterService(api_key=ALPHA_VANTAGE_API_KEY)

logger.info("SUCCESS: All services initialized successfully")


# Import for HTML responses
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Root endpoint - Landing page for the Company Ticker Matching API
    """
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Company Ticker Matching API</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Arial, sans-serif; 
                    max-width: 800px; 
                    margin: 50px auto; 
                    padding: 20px; 
                    background-color: #f5f5f5;
                }
                .container { 
                    background: white; 
                    padding: 40px; 
                    border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                h1 { color: #2c3e50; margin-bottom: 30px; }
                h2 { color: #34495e; margin-top: 30px; }
                .endpoint { 
                    background: #ecf0f1; 
                    padding: 15px; 
                    margin: 10px 0; 
                    border-radius: 5px;
                    border-left: 4px solid #3498db;
                }
                .method { 
                    color: white; 
                    padding: 3px 8px; 
                    border-radius: 3px; 
                    font-size: 12px; 
                    font-weight: bold;
                    margin-right: 10px;
                }
                .get { background-color: #27ae60; }
                .post { background-color: #e74c3c; }
                a { color: #3498db; text-decoration: none; }
                a:hover { text-decoration: underline; }
                .documentation { 
                    background: #e8f5e8; 
                    padding: 20px; 
                    border-radius: 5px; 
                    margin: 20px 0;
                    border-left: 4px solid #27ae60;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏢 Company Ticker Matching API</h1>
                <p>Welcome to the Company Ticker Matching API! This service helps you match company names to their stock ticker symbols.</p>
                
                <div class="documentation">
                    <h3>📚 API Documentation</h3>
                    <p>Explore the interactive API documentation:</p>
                    <ul>
                        <li><a href="/docs" target="_blank"><strong>Swagger UI</strong></a> - Interactive API explorer</li>
                        <li><a href="/redoc" target="_blank"><strong>ReDoc</strong></a> - Clean API documentation</li>
                    </ul>
                </div>

                <h2>🔗 Available Endpoints</h2>
                
                <div class="endpoint">
                    <span class="method post">POST</span>
                    <strong>/match</strong> - Match a company name to stock ticker
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <strong>/update-tickers</strong> - Update ticker data from Alpha Vantage
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <strong>/latest-tickers</strong> - Get last update timestamp
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <strong>/timezones</strong> - List available timezones
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <strong>/health/detailed</strong> - Detailed health check
                </div>

                <h2>🚀 Quick Start</h2>
                <p>Try the API by visiting <a href="/docs">/docs</a> for an interactive interface, or make a POST request to <code>/match</code> with a company name.</p>
                
                <p style="margin-top: 30px; color: #7f8c8d; font-size: 14px;">
                    API Version: {version} | 
                    <a href="https://github.com/yourusername/public-company-api-2" target="_blank">GitHub Repository</a>
                </p>
            </div>
        </body>
    </html>
    """.format(version=settings.APP_VERSION)
    
    return HTMLResponse(content=html_content)


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
                    logger.info("Match data structure: %s", match)
                    
                    # Use the correct key name and ensure score is properly formatted
                    score = match.get("name_match_score", match.get("score", 0))
                    logger.info("Extracted score: %s from name_match_score: %s, score: %s", 
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
        raise HTTPException(status_code=500, detail="Internal server error") from e





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
        raise HTTPException(status_code=500, detail="Internal server error") from e


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
        raise HTTPException(status_code=500, detail="Internal server error") from e


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
        raise HTTPException(status_code=500, detail="Internal server error") from e





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
        openai_available = OPENAI_SERVICE.is_available() if OPENAI_SERVICE else False

        if is_healthy:
            return HealthCheckResponse(
                status="healthy",
                database="connected",
                openai_service="available" if openai_available else "unavailable",
                version=settings.APP_VERSION,
            )
        
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
        ) from e


def run_server():
    """Run the FastAPI server with uvicorn."""
    logger.info("Starting FastAPI ticker matching server...")
    logger.info("Server will be available at: http://%s:%s", HOST, PORT)
    logger.info("API Documentation at: http://%s:%s/docs", HOST, PORT)
    logger.info("Debug mode: %s", DEBUG)
    logger.info("Press Ctrl+C to stop the server")
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
