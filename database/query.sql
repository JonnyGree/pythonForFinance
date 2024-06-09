-- Database: pythonForFinanceDb

-- DROP DATABASE IF EXISTS "pythonForFinanceDb";

CREATE TABLE stock_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    date DATETIME  NOT NULL,
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

CREATE TABLE IF NOT EXISTS listing_status (
    symbol TEXT PRIMARY KEY,
    name TEXT,
    exchange TEXT,
    assetType TEXT,
    ipoDate TEXT,
    delistingDate TEXT,
    status TEXT
);

CREATE TABLE IF NOT EXISTS wilshire_5000 (
    Ticker TEXT,
    Name TEXT,
    Sector TEXT,
    Price REAL,
    Dividend_Yield REAL,
    One_Year_Dividend_Growth REAL,
    Five_Year_Dividend_Growth_Annualized REAL,
    Dividends_Per_Share REAL,
    Market_Cap_M REAL,
    Trailing_PE_Ratio REAL,
    Payout_Ratio REAL,
    Beta REAL,
    Fifty_Two_Week_High REAL,
    Fifty_Two_Week_Low REAL
 );

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