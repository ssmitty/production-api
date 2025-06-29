# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-06-5
### Added
- Initial public release of Company Ticker Matching API.
- `/match` endpoint for JSON API matching.
- `/update_tickers` endpoint for updating tickers.
- Swagger UI documentation at `/apidocs`.
- HTML form for manual testing at `/`.

### Changed
- Improved error handling and logging.
- Environment variable support for configuration.

### Removed
- Training and model files from production codebase.

## [1.1.0]
- Switched primary matching to vector-based (TF-IDF + NearestNeighbors)
- Fallback to fuzzy matching (rapidfuzz) and GPT for ambiguous cases
- Updated requirements: added python-dotenv, scikit-learn
- Added support for evaluating on misspellings (misspellings.csv) in evaluate_model.py
- Updated documentation: guidance on avoiding large files in repo, troubleshooting GitHub push errors, and fresh repo initialization 

## [1.2.0]
- Bug fixes in ranking potential matches
-Improved error handling and logging
-Cloud Deployed