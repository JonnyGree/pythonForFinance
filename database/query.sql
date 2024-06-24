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


WITH start_data AS (
    SELECT date AS start_date, adj_close AS start_adj_close
    FROM stock_data
    WHERE ticker = :ticker
    AND date >= :start_date
    ORDER BY date ASC
    LIMIT 1
),
end_data AS (
    SELECT date AS end_date, adj_close AS end_adj_close
    FROM stock_data
    WHERE ticker = :ticker
    AND date <= :end_date
    ORDER BY date DESC
    LIMIT 1
)
SELECT
    start_date,
    start_adj_close,
    end_date,
    end_adj_close,
    (end_adj_close - start_adj_close) / start_adj_close AS roi
FROM start_data
JOIN end_data ON 1=1;

CREATE OR REPLACE FUNCTION calculate_roi(p_ticker TEXT, p_year INTEGER) RETURNS NUMERIC AS $$
DECLARE
    start_adj_close NUMERIC;
    end_adj_close NUMERIC;
    roi NUMERIC;
BEGIN
    -- Get the starting adjusted close price for the year
    SELECT adj_close INTO start_adj_close
    FROM stock_data
    WHERE stock_data.ticker = p_ticker
    AND date >= (p_year || '-01-01')::DATE
    ORDER BY date ASC
    LIMIT 1;

    -- Get the ending adjusted close price for the year
    SELECT adj_close INTO end_adj_close
    FROM stock_data
    WHERE stock_data.ticker = p_ticker
    AND date <= (p_year || '-12-31')::DATE
    ORDER BY date DESC
    LIMIT 1;

    -- Calculate ROI
    IF start_adj_close IS NOT NULL AND end_adj_close IS NOT NULL THEN
        roi := (end_adj_close - start_adj_close) / start_adj_close;
    ELSE
        roi := NULL;
    END IF;

    RETURN roi;
END;
$$ LANGUAGE plpgsql;

DO $$
DECLARE
    rec RECORD;
    year INTEGER;
    roi NUMERIC;
BEGIN
    -- Create temporary table for unique tickers
    CREATE TEMP TABLE unique_tickers AS
    SELECT DISTINCT ticker
    FROM stock_data;

    -- Loop through each unique ticker
    FOR rec IN (SELECT ticker FROM unique_tickers) LOOP
        -- Loop through each year from 2010 to 2024
        FOR year IN 2010..2024 LOOP
            roi := calculate_roi(rec.ticker, year);

            -- Insert or update the stock_returns table
            INSERT INTO stock_returns (ticker, return_2024, return_2023, return_2022, return_2021, return_2020, return_2019, return_2018, return_2017, return_2016, return_2015, return_2014, return_2013, return_2012, return_2011, return_2010)
            VALUES (rec.ticker, 
                    CASE WHEN year = 2024 THEN roi ELSE NULL END,
                    CASE WHEN year = 2023 THEN roi ELSE NULL END,
                    CASE WHEN year = 2022 THEN roi ELSE NULL END,
                    CASE WHEN year = 2021 THEN roi ELSE NULL END,
                    CASE WHEN year = 2020 THEN roi ELSE NULL END,
                    CASE WHEN year = 2019 THEN roi ELSE NULL END,
                    CASE WHEN year = 2018 THEN roi ELSE NULL END,
                    CASE WHEN year = 2017 THEN roi ELSE NULL END,
                    CASE WHEN year = 2016 THEN roi ELSE NULL END,
                    CASE WHEN year = 2015 THEN roi ELSE NULL END,
                    CASE WHEN year = 2014 THEN roi ELSE NULL END,
                    CASE WHEN year = 2013 THEN roi ELSE NULL END,
                    CASE WHEN year = 2012 THEN roi ELSE NULL END,
                    CASE WHEN year = 2011 THEN roi ELSE NULL END,
                    CASE WHEN year = 2010 THEN roi ELSE NULL END)
            ON CONFLICT (ticker) DO UPDATE
            SET return_2024 = CASE WHEN EXCLUDED.return_2024 IS NOT NULL THEN EXCLUDED.return_2024 ELSE stock_returns.return_2024 END,
                return_2023 = CASE WHEN EXCLUDED.return_2023 IS NOT NULL THEN EXCLUDED.return_2023 ELSE stock_returns.return_2023 END,
                return_2022 = CASE WHEN EXCLUDED.return_2022 IS NOT NULL THEN EXCLUDED.return_2022 ELSE stock_returns.return_2022 END,
                return_2021 = CASE WHEN EXCLUDED.return_2021 IS NOT NULL THEN EXCLUDED.return_2021 ELSE stock_returns.return_2021 END,
                return_2020 = CASE WHEN EXCLUDED.return_2020 IS NOT NULL THEN EXCLUDED.return_2020 ELSE stock_returns.return_2020 END,
                return_2019 = CASE WHEN EXCLUDED.return_2019 IS NOT NULL THEN EXCLUDED.return_2019 ELSE stock_returns.return_2019 END,
                return_2018 = CASE WHEN EXCLUDED.return_2018 IS NOT NULL THEN EXCLUDED.return_2018 ELSE stock_returns.return_2018 END,
                return_2017 = CASE WHEN EXCLUDED.return_2017 IS NOT NULL THEN EXCLUDED.return_2017 ELSE stock_returns.return_2017 END,
                return_2016 = CASE WHEN EXCLUDED.return_2016 IS NOT NULL THEN EXCLUDED.return_2016 ELSE stock_returns.return_2016 END,
                return_2015 = CASE WHEN EXCLUDED.return_2015 IS NOT NULL THEN EXCLUDED.return_2015 ELSE stock_returns.return_2015 END,
                return_2014 = CASE WHEN EXCLUDED.return_2014 IS NOT NULL THEN EXCLUDED.return_2014 ELSE stock_returns.return_2014 END,
                return_2013 = CASE WHEN EXCLUDED.return_2013 IS NOT NULL THEN EXCLUDED.return_2013 ELSE stock_returns.return_2013 END,
                return_2012 = CASE WHEN EXCLUDED.return_2012 IS NOT NULL THEN EXCLUDED.return_2012 ELSE stock_returns.return_2012 END,
                return_2011 = CASE WHEN EXCLUDED.return_2011 IS NOT NULL THEN EXCLUDED.return_2011 ELSE stock_returns.return_2011 END,
                return_2010 = CASE WHEN EXCLUDED.return_2010 IS NOT NULL THEN EXCLUDED.return_2010 ELSE stock_returns.return_2010 END;
        END LOOP;
    END LOOP;
END;
$$;

