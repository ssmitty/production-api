# Changelog

All notable changes to this project will be documented in this file.

## [1.3.0] - 2025-01-28
### Added
- **Library Distribution**: Prepared for use as a data science team tool/library
- Enhanced project metadata for PyPI distribution
- Comprehensive .gitignore for library development
- MIT license specification
- Keywords and classifiers for better package discovery

### Changed
- **BREAKING**: Migrated fully from Flask to FastAPI (Flask components removed)
- Updated project name to `production-company-ticker-api`
- Aligned all dependencies between pyproject.toml and requirements.txt
- Improved project structure documentation

### Removed
- **BREAKING**: Removed obsolete Flask service components (`src/core/services/flask_app/`)
- Removed Flask dependencies from pyproject.toml
- Cleaned up obsolete configuration patterns

### Fixed
- Dependency version mismatches between configuration files
- Library packaging metadata

## [1.2.0] - 2024-06-5
### Changed
- Bug fixes in ranking potential matches
- Improved error handling and logging
- Cloud Deployed

## [1.1.0] - 2024-06-5
### Changed
- Switched primary matching to vector-based (TF-IDF + NearestNeighbors)
- Fallback to fuzzy matching (rapidfuzz) and GPT for ambiguous cases
- Updated requirements: added python-dotenv, scikit-learn
- Added support for evaluating on misspellings (misspellings.csv) in evaluate_model.py
- Updated documentation: guidance on avoiding large files in repo, troubleshooting GitHub push errors, and fresh repo initialization 

## [1.0.0] - 2024-06-5
### Added
- Initial public release of Company Ticker Matching API
- `/match` endpoint for JSON API matching
- `/update_tickers` endpoint for updating tickers
- Swagger UI documentation at `/apidocs`
- HTML form for manual testing at `/`

### Changed
- Improved error handling and logging
- Environment variable support for configuration

### Removed
- Training and model files from production codebase 