-- Database initialization script for ticker API
-- This script runs automatically when PostgreSQL container starts

-- Ensure the database exists (though it should be created by POSTGRES_DB env var)
SELECT 'CREATE DATABASE company_ticker_db' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'company_ticker_db');

-- Connect to the database
\c company_ticker_db;

-- Create any initial extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- The application will automatically create tables using pandas.to_sql()
-- Tables that will be created by the application:
-- - tickers: Contains ticker symbols and company names
-- - metadata: Contains system metadata and update timestamps

-- Optional: Create indexes for better performance (uncomment if needed)
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tickers_ticker ON tickers(ticker);
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tickers_title ON tickers(title);

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'Database initialization completed successfully';
END $$; 