# 🎯 Company Ticker Matching API

A production-ready FastAPI service for matching company names to stock ticker symbols using advanced machine learning techniques including exact matching, fuzzy matching, and OpenAI-powered fallback matching.

## 🚀 Live Demo

**🌐 Deployed API**: [http://production.eba-majswwkn.us-east-1.elasticbeanstalk.com/docs](http://production.eba-majswwkn.us-east-1.elasticbeanstalk.com/docs)

- **Interactive API Docs**: `/docs`
- **Web Form Interface**: `/home` 
- **Health Check**: `/health`

## ✨ Features

- **🎯 Smart Matching**: Multi-strategy matching (exact → fuzzy → AI fallback)
- **⚡ High Performance**: Sub-second response times with caching
- **🤖 AI Integration**: OpenAI GPT fallback for complex company names
- **📊 REST API**: JSON and form-based endpoints
- **🔄 Live Data**: Real-time ticker updates from Alpha Vantage
- **💾 PostgreSQL**: Persistent storage with metadata tracking

## 🏗️ Architecture

```
Input Company Name → Text Preprocessing → Exact Match → Fuzzy Match → AI Fallback → Result
```

## ⚡ Quick Start

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
# Activate environment
source venv/bin/activate

# Load environment variables
set -a && source .env.secrets && set +a

# Start server
python src/api/app_fastapi.py
```

Access at: http://localhost:8080/docs

## 📦 Library Usage

Use as a Python library in your data science projects:

```python
# Install
pip install git+https://github.com/ssmitty/public-company-api.git

# Use in code
from src.api.ticker_matcher import TickerMatcherService

matcher = TickerMatcherService(
    database_url=DATABASE_URL,
    alpha_vantage_api_key=API_KEY,
    openai_api_key=OPENAI_KEY  # Optional
)

# Match company to ticker
result = matcher.match_company("Apple Inc")
print(f"Ticker: {result.predicted_ticker}")  # AAPL
```

### Jupyter Notebook Example

```python
import pandas as pd

companies_df = pd.DataFrame({
    'company_name': ['Apple Inc', 'Microsoft Corporation', 'Google LLC']
})

# Add tickers
companies_df['ticker'] = companies_df['company_name'].apply(
    lambda name: matcher.match_company(name).predicted_ticker
)
```

## 📚 API Reference

### Match Company Name
```http
POST /api/match
Content-Type: application/json

{
  "company_name": "Apple Inc"
}
```

**Response:**
```json
{
  "input_name": "Apple Inc",
  "matched_name": "Apple Inc", 
  "predicted_ticker": "AAPL",
  "name_match_score": 0.95,
  "message": "Exact match found",
  "api_latency": 0.123
}
```

### Other Endpoints
- **`GET /update-tickers`** - Refresh ticker data from Alpha Vantage
- **`GET /latest-tickers`** - Get last update timestamp
- **`GET /health`** - Health check
- **`GET /home`** - Web form interface

## 🛠️ Development

```bash
# Run tests
python -m pytest src/tests/

# Code formatting
black src/

# Type checking  
mypy src/
```

## 🐳 Deployment

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

## 📁 Project Structure

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

## ⚙️ Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `ALPHA_VANTAGE_API_KEY` | ✅ | Alpha Vantage API key |
| `OPENAI_API_KEY` | ❌ | OpenAI API key (optional) |
| `PORT` | ❌ | Server port (default: 8000) |

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Follow coding standards (SRP, type hints)
4. Add tests
5. Submit pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**🚀 Built with FastAPI • Deployed on AWS • Ready for production** 