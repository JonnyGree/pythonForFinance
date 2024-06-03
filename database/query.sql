-- Database: pythonForFinanceDb

-- DROP DATABASE IF EXISTS "pythonForFinanceDb";

CREATE DATABASE "pythonForFinanceDb"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United Kingdom.1252'
    LC_CTYPE = 'English_United Kingdom.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

CREATE TABLE stock_data (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open NUMERIC(15, 6) NOT NULL,
    high NUMERIC(15, 6) NOT NULL,
    low NUMERIC(15, 6) NOT NULL,
    close NUMERIC(15, 6) NOT NULL,
	adj_close NUMERIC(15, 6) NOT NULL,
    volume BIGINT NOT NULL,
    dividends NUMERIC(15, 6),
    stock_splits NUMERIC(15, 6),
    capital_gains NUMERIC(15, 6),
    UNIQUE(ticker, date)
);

CREATE INDEX idx_stock_data_ticker_date ON stock_data(ticker, date);

SELECT *
	FROM public.stock_data;

INSERT INTO stock_data (ticker, date, open, high, low, close, volume, dividends, stock_splits, capital_gains)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (ticker, date) DO UPDATE
SET open = EXCLUDED.open,
    high = EXCLUDED.high,
    low = EXCLUDED.low,
    close = EXCLUDED.close,
    volume = EXCLUDED.volume,
    dividends = EXCLUDED.dividends,
    stock_splits = EXCLUDED.stock_splits,
    capital_gains = EXCLUDED.capital_gains;
