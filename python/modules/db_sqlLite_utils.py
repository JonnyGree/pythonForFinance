import sqlite3
import pandas as pd
import os

class db_utils:
    conn = None

    @staticmethod
    def connect():
        """
        Establish a connection to the SQLite database.
        """
        if db_utils.conn is None:
            db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'pythonForFinanceDb.db')
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            db_utils.conn = sqlite3.connect(db_path)
            print("Database connection established.")

    @staticmethod
    def close():
        """
        Close the connection to the SQLite database.
        """
        if db_utils.conn:
            db_utils.conn.close()
            db_utils.conn = None
            print("Database connection closed.")

    @staticmethod
    def create_db():
        """
        Create the SQLite database and the necessary table.
        """
        db_utils.connect()
        cur = db_utils.conn.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS stock_data (
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
            )
        ''')

        cur.execute('''
            CREATE INDEX IF NOT EXISTS idx_stock_data_ticker_date 
            ON stock_data(date)
        ''')

        # Create listing_status table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS listing_status (
                symbol TEXT PRIMARY KEY,
                name TEXT,
                exchange TEXT,
                assetType TEXT,
                ipoDate TEXT,
                delistingDate TEXT,
                status TEXT
            )
        ''')

        db_utils.conn.commit()

        # Create wilshire 5000 table
        cur.execute('''
        CREATE TABLE IF NOT EXISTS wilshire_5000 (
            Ticker TEXT UNIQUE,
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
        )
        ''')
        db_utils.conn.commit()

        cur.close()

    @staticmethod
    def execute_values(df, table, ticker):
        """
        Insert or update the dataframe into the specified table.
        """
        db_utils.connect()
        
        # Convert Timestamp objects to strings
        if 'date' in df.columns:
            df['date'] = df['date'].astype(str)

        tuples = [tuple([ticker] + list(x)) for x in df.to_numpy()]
        cols = 'ticker,' + ','.join(list(df.columns))
        query = f"INSERT INTO {table}({cols}) VALUES ({','.join(['?' for _ in range(len(df.columns) + 1)])}) ON CONFLICT(ticker, date) DO UPDATE SET "
        update_cols = ','.join([f"{col}=excluded.{col}" for col in list(df.columns)])
        query += update_cols

        cur = db_utils.conn.cursor()
        try:
            cur.executemany(query, tuples)
            db_utils.conn.commit()
            print("execute_values() done")
        except sqlite3.DatabaseError as error:
            print(f"Error: {error}")
            db_utils.conn.rollback()
            cur.close()
            return 1
        cur.close()

    
    @staticmethod
    def get_ticker_from_stock():
        db_utils.connect()
        cur = db_utils.conn.cursor()
        
        # Query to select distinct sectors
        cur.execute('''
        SELECT DISTINCT ticker FROM stock_data
        ''')
        
        # Fetch all results
        rows = cur.fetchall()
        cur.close()
        # Extract sectors from rows
        sectors = [row[0] for row in rows]
        return sectors

    @staticmethod
    def get_data_from_db(ticker, start=None, end=None):
        """
        Retrieve historical stock data from the database.
        """
        db_utils.connect()
        try:
            cur = db_utils.conn.cursor()
            query = "SELECT date, open, high, low, close, adj_close, volume, dividends, stock_splits, capital_gains FROM stock_data WHERE ticker = ?"
            params = [ticker]
            if start:
                query += " AND date >= ?"
                params.append(start)
            if end:
                query += " AND date <= ?"
                params.append(end)
            cur.execute(query, params)
            data = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            df = pd.DataFrame(data, columns=columns)

            # Remove rows with NaN values
            df = df.dropna(axis=1, how='all')

            # Convert 'date' column to datetime format
            df['date'] = pd.to_datetime(df['date'])

            cur.close()
            return df
        except sqlite3.DatabaseError as error:
            print(f"Error: {error}")
            return None
        
    @staticmethod
    def insert_listing_status(data):
        """
        Insert listing status data into the listing_status table.
        """
        db_utils.connect()
        cur = db_utils.conn.cursor()

        for index, row in data.iterrows():
            cur.execute('''
                INSERT OR IGNORE INTO listing_status (symbol, name, exchange, assetType, ipoDate, delistingDate, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['symbol'], row['name'], row['exchange'], row['assetType'],
                row['ipoDate'], row['delistingDate'], row['status']
            ))

        db_utils.conn.commit()
        cur.close()

    @staticmethod
    def insert_wilshire_stocks(data):   
        data.to_sql('wilshire_5000', db_utils.conn, if_exists='replace', index=False)

    @staticmethod
    def get_wilshire_distinct_sectors():
        db_utils.connect()
        cur = db_utils.conn.cursor()
        
        # Query to select distinct sectors
        cur.execute('''
        SELECT DISTINCT Sector FROM wilshire_5000
        WHERE Sector IS NOT NULL
        ''')
        
        # Fetch all results
        rows = cur.fetchall()
        cur.close()
        # Extract sectors from rows
        sectors = [row[0] for row in rows]
        return sectors

    def get_wilshire_ticker():
        db_utils.connect()
        cur = db_utils.conn.cursor()
        cur.execute('''
        SELECT DISTINCT Ticker FROM wilshire_5000
        WHERE Ticker IS NOT NULL
        ''')
        # Fetch all results
        tickers = [row[0] for row in cur.fetchall()]
        cur.close()
        return tickers

    @staticmethod
    def get_wilshire_ticker_by_sector(sector):
        db_utils.connect()
        cur = db_utils.conn.cursor()
    
        cur.execute('''
        SELECT * FROM wilshire_5000
        WHERE Sector = ?
        ''', (sector,))
       
        # Fetch all results
        tickers = [row[0] for row in cur.fetchall()]
        cur.close()
        return tickers

    @staticmethod
    def get_tickers_by_exchange(exchange):
        """
        Retrieve all tickers listed on a specified exchange.
        """
        db_utils.connect()
        cur = db_utils.conn.cursor()

        cur.execute('''
            SELECT symbol FROM listing_status WHERE exchange = ?
        ''', (exchange,))

        exchange_tickers = [row[0] for row in cur.fetchall()]

        cur.close()
        return exchange_tickers
    
