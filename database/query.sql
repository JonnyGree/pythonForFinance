-- Database: pythonForFinanceDb

-- DROP DATABASE IF EXISTS "pythonForFinanceDb";

CREATE TABLE stock_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    date DATE NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    adj_close REAL NOT NULL,
    volume INTEGER NOT NULL,
    dividends REAL,
    stock_splits REAL,
    capital_gains REAL,
    UNIQUE(ticker, date)
);

CREATE INDEX idx_stock_data_ticker_date ON stock_data(ticker, date);

INSERT INTO stock_data (ticker, date, open, high, low, close, volume, dividends, stock_splits, capital_gains)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(ticker, date) DO UPDATE SET
    open = excluded.open,
    high = excluded.high,
    low = excluded.low,
    close = excluded.close,
    volume = excluded.volume,
    dividends = excluded.dividends,
    stock_splits = excluded.stock_splits,
    capital_gains = excluded.capital_gains;