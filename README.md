# Company Ticker Matching API

A production-ready FastAPI service for matching company names to stock ticker symbols using advanced machine learning techniques including exact matching, fuzzy matching, and OpenAI-powered fallback matching.

## Live Demo

**Deployed API**: [http://production.eba-majswwkn.us-east-1.elasticbeanstalk.com/docs](http://production.eba-majswwkn.us-east-1.elasticbeanstalk.com/docs)

- **Interactive API Docs**: `/docs`

## Features

- **Smart Matching**: Multi-strategy matching (exact → fuzzy → AI fallback)
- **High Performance**: Sub-second response times with caching
- **AI Integration**: OpenAI GPT fallback for complex company names
- **REST API**: JSON and form-based endpoints
- **Live Data**: Real-time ticker updates from Alpha Vantage
- **PostgreSQL**: Persistent storage with metadata tracking

## Architecture

```
Input Company Name → Text Preprocessing → Exact Match → Fuzzy Match → AI Fallback → Result
```

## Database Choice: PostgreSQL

PostgreSQL was selected as the primary database for several key reasons:

- **Cost Effectiveness**: Significantly lower operational costs compared to proprietary databases like Oracle or SQL Server
- **Easy Setup**: Simple installation and configuration process with excellent Docker support
- **Production Ready**: Battle-tested reliability with ACID compliance and robust transaction handling
- **Scalability**: Handles large datasets efficiently with advanced indexing and query optimization
- **JSON Support**: Native JSON data types for flexible schema evolution without migration overhead
- **Rich Ecosystem**: Extensive tooling, monitoring solutions, and cloud provider support (AWS RDS, Google Cloud SQL)
- **Open Source**: No licensing fees and active community development ensuring long-term viability

## Quick Start

### Prerequisites
- Python 3.11+ (recommended)
- PostgreSQL database
- Alpha Vantage API key
- OpenAI API key (optional)

### Setup

```bash
# Clone repository
git clone <repository-url>
cd public-company-api

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create `.env.secrets` file:
```bash
DATABASE_URL=postgresql://user:password@host:port/database
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
OPENAI_API_KEY=your_openai_key  # Optional
```

### Run

```bash
# Load environment variables
set -a && source .env.secrets && set +a

# Start server
python src/api/app_fastapi.py
```

Access at: http://localhost:8080/docs

## API Reference

### Available Endpoints
- **`GET /update-tickers`** - Refresh ticker data from Alpha Vantage
- **`GET /latest-tickers`** - Get last update timestamp
- **`GET /health/detailed`** - Detailed health check
- **`POST /match`** - Form-based company matching

## Development

```bash
# Run tests
python -m pytest src/tests/

# Code formatting
black src/

# Type checking  
mypy src/
```

## Deployment

### Docker
```bash
docker build -t ticker-api .
docker run -p 8080:8080 --env-file .env.secrets ticker-api
```

### Production
- Configure environment variables
- Set up PostgreSQL database
- Deploy to cloud platform (AWS, GCP, Azure)
- Configure reverse proxy for production

## Project Structure

```
public-company-api/
├── src/
│   ├── api/                 # FastAPI application
│   ├── core/               # Business logic & services  
│   ├── database/           # Data layer
│   ├── models/             # Data models
│   └── utils/              # Utilities
├── requirements.txt        # Dependencies
├── Procfile               # Deployment config
└── README.md              # This file
```

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Required | PostgreSQL connection string |
| `ALPHA_VANTAGE_API_KEY` | Required | Alpha Vantage API key |
| `OPENAI_API_KEY` | Optional | OpenAI API key (optional) |
| `PORT` | Optional | Server port (default: 8000) |

**Built with FastAPI • Deployed on AWS • Ready for production** 