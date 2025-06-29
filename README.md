# 🎯 Ticker Matching Service

A production-ready FastAPI service for matching company names to stock ticker symbols using advanced machine learning techniques including exact matching, fuzzy matching, and OpenAI-powered fallback matching.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Development](#-development)
- [Deployment](#-deployment)
- [Library Usage](#-library-usage)
- [Contributing](#-contributing)

## 🚀 Features

### Core Functionality
- **🎯 Multi-Strategy Matching**: Exact matching, fuzzy matching, and AI-powered fallback
- **⚡ High Performance**: Optimized algorithms with caching for sub-second response times
- **🤖 AI Integration**: OpenAI GPT integration for complex company name resolution
- **📊 Comprehensive API**: RESTful endpoints with form-based and JSON interfaces
- **🔄 Real-time Updates**: Live ticker data updates from Alpha Vantage API
- **💾 Persistent Storage**: PostgreSQL database with metadata tracking

### Technical Features
- **🏗️ Micro-services Architecture**: Single Responsibility Principle (SRP) compliant design
- **📈 Scalable Design**: Horizontal scaling support with stateless services
- **🛡️ Error Handling**: Comprehensive error handling and graceful degradation
- **📝 Auto-documentation**: OpenAPI/Swagger documentation with interactive testing
- **🔍 Health Monitoring**: Built-in health checks and system monitoring
- **🌐 CORS Support**: Cross-origin resource sharing for web applications

## 🏗️ Architecture

### Design Principles
- **Single Responsibility Principle**: Each class has 1-2 methods maximum
- **Dependency Injection**: Clean separation of concerns and testable design
- **Micro-services Pattern**: Focused services with specific responsibilities
- **Property-based Interfaces**: Fluent APIs for text processing chains

### Matching Strategy Flow
```
Input Company Name
        ↓
   Text Preprocessing
        ↓
    Exact Matching ──→ Found? ──→ Return Result
        ↓ No
   Fuzzy Matching ──→ Found? ──→ Return Result
        ↓ No
  OpenAI Fallback ──→ Found? ──→ Return Result
        ↓ No
   "No Match Found"
```

## 📁 Project Structure

```
production-api/

├── 📚 README.md                  # This file
├── ⚙️ requirements.txt           # Python dependencies
├── 🐳 Dockerfile                # Container configuration
├── 📝 .env.example              # Environment template
│
├── 📂 src/                      # Source code
│   ├── 🌐 api/                  # API layer
│   │   ├── app_fastapi.py       # Main FastAPI application
│   │   └── ticker_matcher.py    # Consolidated library interface
│   │
│   ├── ⚙️ config/               # Configuration
│   │   └── settings.py          # Application settings
│   │
│   ├── 🧠 core/                 # Core business logic
│   │   ├── services/            # Business services
│   │   │   ├── company_matcher_service.py
│   │   │   ├── exact_matcher_service.py
│   │   │   ├── fuzzy_matcher_service.py
│   │   │   ├── openai_service.py
│   │   │   ├── ticker_updater_service.py
│   │   │   ├── matchers/        # Matching micro-services
│   │   │   ├── matching/        # Strategy orchestrators
│   │   │   ├── data_processing/ # Data processing services
│   │   │   └── health_checkers/ # Health monitoring
│   │   └── interfaces/          # Abstract interfaces
│   │
│   ├── 💾 database/             # Data layer
│   │   └── repositories/        # Database services
│   │       ├── metadata_service.py
│   │       ├── ticker_loader_service.py
│   │       └── database_health_service.py
│   │
│   ├── 📊 models/               # Data models
│   │   ├── api.py              # API request/response models
│   │   └── ticker.py           # Core business models
│   │
│   ├── 🛠️ utils/                # Utilities
│   │   └── export_db_to_csv.py # Database export tools
│   │
│   ├── 📖 docs/                 # Documentation
│   │   ├── openapi.yaml        # OpenAPI specification
│   │   └── prompts/            # AI prompts and configs
│   │
│   ├── 🧪 examples/             # Usage examples
│   └── 🧪 tests/                # Test suite
│
└── 🔧 deployment/               # Deployment configs
    ├── docker-compose.yml
    └── Procfile
```

## ⚡ Quick Start

### Prerequisites
- Python 3.11.9 (recommended)
- PostgreSQL database
- Alpha Vantage API key
- OpenAI API key (optional)

### 0. Virtual Environment Setup

**Step 1: Install Python 3.11.9**

**macOS (using Homebrew):**
```bash
# Install Python 3.11.9 if not already installed
brew install python@3.11

# Verify installation
python3.11 --version  # Should show Python 3.11.9
```

**macOS (using pyenv - recommended for multiple Python versions):**
```bash
# Install pyenv if not already installed
brew install pyenv

# Install Python 3.11.9
pyenv install 3.11.9

# Set as global or local version
pyenv global 3.11.9  # or `pyenv local 3.11.9` for this project only
```

**Ubuntu/Debian:**
```bash
# Update package list
sudo apt update

# Install Python 3.11.9 and venv
sudo apt install python3.11 python3.11-venv python3.11-dev

# Verify installation
python3.11 --version
```

**Windows:**
```bash
# Download and install Python 3.11.9 from python.org
# Or use chocolatey:
choco install python --version=3.11.9
```

**Step 2: Create Virtual Environment**
```bash
# Navigate to the project directory
cd production-api

# Create virtual environment with Python 3.11.9
python3.11 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Verify you're using the correct Python version
python --version  # Should show Python 3.11.9

# Upgrade pip to latest version
pip install --upgrade pip
```

**Step 3: Verify Setup**
```bash
# Check Python version
python --version

# Check pip version
pip --version

# Should see something like:
# Python 3.11.9
# pip 24.x.x from /path/to/venv/lib/python3.11/site-packages/pip (python 3.11)
```

 > **💡 Pro Tip:** Always activate your virtual environment before working on the project:
> ```bash
> source venv/bin/activate  # macOS/Linux
> # or
> venv\Scripts\activate     # Windows
> ```

**Troubleshooting Virtual Environment:**
```bash
# If python3.11 is not found, try:
python3 --version                    # Check available Python version
which python3.11                   # Check if Python 3.11 is installed

# If venv creation fails:
python3.11 -m pip install --upgrade pip
python3.11 -m pip install virtualenv
python3.11 -m virtualenv venv

# If activation doesn't work:
# Make sure you're in the project directory
# Check that venv/ folder exists
ls -la venv/                        # Should show bin/ folder (macOS/Linux)
dir venv\                           # Should show Scripts\ folder (Windows)

# If wrong Python version in venv:
rm -rf venv                         # Delete and recreate
python3.11 -m venv venv
```

### 1. Installation
```bash
# Clone the repository
git clone <repository-url>
cd production-api

# Make sure your virtual environment is activated first!
# source venv/bin/activate  (macOS/Linux)
# venv\Scripts\activate     (Windows)

# Install dependencies
pip install -r requirements.txt

# Or using Poetry (if you prefer)
poetry install
```

> **⚠️ Important:** Make sure your virtual environment is activated before installing dependencies!

### 2. Environment Setup

**Step 1: Create a `.env.secrets` file:**
```bash
DATABASE_URL=postgresql://user:password@host:port/database
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
OPENAI_API_KEY=your_openai_key  # Optional
PORT=8080
HOST=0.0.0.0
DEBUG=true
```

**Step 2: Export Environment Variables**

Since we follow library-first principles (no automatic .env loading), you must export environment variables manually:

**Option A: Export manually each time**
```bash
# Export required environment variables
export DATABASE_URL="postgresql://user:password@host:port/database"
export ALPHA_VANTAGE_API_KEY="your_alpha_vantage_key"
export OPENAI_API_KEY="your_openai_key"  # Optional
export PORT=8080
export HOST="0.0.0.0"
export DEBUG=true
```

**Option B: Source the .env.secrets file (recommended for development)**
```bash
# Load all environment variables from .env.secrets
set -a  # automatically export all variables
source .env.secrets
set +a  # stop automatically exporting

# Verify variables are loaded
echo $DATABASE_URL
echo $ALPHA_VANTAGE_API_KEY
```

**Option C: One-liner with environment injection**
```bash
# Run with environment variables from .env.secrets
env $(cat .env.secrets | grep -v '^#' | xargs) python src/api/app_fastapi.py
```

### 3. Run the Server
```bash
# Make sure your virtual environment is activated
source venv/bin/activate  # macOS/Linux

# STEP 1: Load environment variables (choose one method)
# Method A: Source .env.secrets (recommended)
set -a && source .env.secrets && set +a

# Method B: One-liner with env injection
# env $(cat .env.secrets | grep -v '^#' | xargs) python src/api/app_fastapi.py

# STEP 2: Run the server
# Simple way
python src/api/app_fastapi.py

# Alternative using uvicorn
python -m uvicorn src.api.app_fastapi:app --host 0.0.0.0 --port 8080 --reload
```

**Quick Development Workflow:**
```bash
# Complete workflow in one go
source venv/bin/activate                    # Activate virtual environment
set -a && source .env.secrets && set +a    # Load environment variables
python src/api/app_fastapi.py               # Run the server
```

> **💡 Virtual Environment Management:**
> - **Activate:** `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)
> - **Deactivate:** `deactivate` (when you're done working)
> - **Check if active:** Your terminal prompt should show `(venv)` at the beginning

### 4. Access the API
- **API Documentation**: http://localhost:8080/docs
- **Interactive Form**: http://localhost:8080/home
- **Health Check**: http://localhost:8080/health

## 📚 API Documentation

### Core Endpoints

#### Match Company Name
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
  "all_possible_tickers": ["AAPL"],
  "name_match_score": 0.95,
  "message": "Exact match found",
  "top_matches": [...],
  "api_latency": 0.123,
  "version": "1.0.0"
}
```

#### Update Ticker Data
```http
GET /update-tickers
```

#### Get Latest Update Time
```http
GET /latest-tickers?tz=America/New_York
```

#### Health Check
```http
GET /health
```

### Interactive Documentation
Visit `/docs` for complete API documentation with interactive testing capabilities.

## ⚙️ Configuration

### Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | ✅ Yes | PostgreSQL connection string |
| `ALPHA_VANTAGE_API_KEY` | ✅ Yes | Alpha Vantage API key for ticker data |
| `OPENAI_API_KEY` | ❌ No | OpenAI API key for fallback matching |
| `PORT` | ❌ No | Server port (default: 8080) |
| `HOST` | ❌ No | Server host (default: 0.0.0.0) |
| `DEBUG` | ❌ No | Debug mode (default: true) |

### Database Schema
The service automatically creates required tables:
- `tickers`: Stock ticker and company name data
- `metadata`: System metadata and timestamps

## 🛠️ Development

> **🚨 Development Prerequisite:** Always ensure your virtual environment is activated before running any development commands:
> ```bash
> source venv/bin/activate  # macOS/Linux
> # or
> venv\Scripts\activate     # Windows
> 
> # Verify correct Python version
> python --version  # Should show Python 3.11.9
> ```

### Running Tests
```bash
# Run all tests
python -m pytest src/tests/

# Run with coverage
python -m pytest src/tests/ --cov=src/
```

### Code Quality
```bash
# Ensure virtual environment is activated first
source venv/bin/activate

# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

### Adding New Features
1. Follow the micro-services pattern (1-2 methods per class)
2. Add services to appropriate directories in `src/core/services/`
3. Update the main orchestrator services
4. Add comprehensive tests
5. Update API documentation

## 🐳 Deployment

### Docker
```bash
# Build image
docker build -t ticker-matching-api .

# Run container
docker run -p 8080:8080 --env-file .env.secrets ticker-matching-api
```

### Docker Compose
```bash
# Run with PostgreSQL
docker-compose up -d
```

### Production Deployment
- Use environment-specific `.env` files
- Configure reverse proxy (nginx/Apache)
- Set up monitoring and logging
- Use production-grade PostgreSQL instance
- Configure auto-scaling based on load

## 📖 Library Usage

### Engineering Team Integration
```python
from src.api.ticker_matcher import TickerMatcher

# Initialize matcher
matcher = TickerMatcher(
    api_key="your_openai_key",
    database_url="your_db_url"
)

# Simple matching
result = matcher.match("Apple Inc")
print(f"Ticker: {result['predicted_ticker']}")

# Batch processing
companies = ["Apple", "Microsoft", "Google"]
results = matcher.batch_match(companies)

# Health monitoring
health = matcher.health_check()
print(f"System status: {health['status']}")
```

### Orchestrator Integration
```python
class FinancialDataProcessor:
    def __init__(self):
        self.ticker_matcher = TickerMatcher()
    
    def process_portfolio(self, company_names):
        results = self.ticker_matcher.batch_match(company_names)
        return self.format_portfolio_data(results)
```

## 🔧 Monitoring & Observability

### Health Checks
- Database connectivity
- External API availability
- Service initialization status
- Performance metrics

### Logging
- Structured JSON logging
- Request/response tracking
- Error monitoring
- Performance metrics

### Metrics
- API response times
- Matching accuracy rates
- Database query performance
- Error rates by endpoint

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Follow coding standards (SRP, micro-services pattern)
4. Add tests for new functionality
5. Update documentation
6. Submit pull request

### Coding Standards
- **Single Responsibility Principle**: Maximum 1-2 methods per class
- **Type Hints**: All functions must have type annotations
- **Documentation**: Comprehensive docstrings for all classes/methods
- **Error Handling**: Graceful error handling with proper logging
- **Testing**: Unit tests for all business logic

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues
1. **Import Errors**: Ensure you're running from the project root
2. **Database Connection**: Verify DATABASE_URL format and accessibility
3. **API Rate Limits**: Check Alpha Vantage and OpenAI usage limits
4. **Environment Variables**: Ensure `.env.secrets` file is properly configured

### Getting Help
- Check the `/health` endpoint for system status
- Review logs for detailed error information
- Consult the interactive API documentation at `/docs`
- Review the examples in `src/examples/`

---

**🚀 Built with FastAPI, designed for scale, optimized for performance.** 