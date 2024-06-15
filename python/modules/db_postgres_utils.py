import pandas as pd
import psycopg2
from psycopg2 import extras
import logging
import configparser
import os

path = '../config.ini'
os.path.abspath(path)

class db_utils:
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)  # Set logging level to INFO by default

    config = configparser.ConfigParser()
    try:
        with open(path, 'r') as file:
            config.read_file(file)
    except Exception as e:
        print(f"Error reading config file: {e}")
        print("Absolute path:", os.path.abspath(path))

    conn_params = {
        'dbname': config['database']['dbname'],
        'user': config['database']['user'],
        'password': config['database']['password'],
        'host': config['database']['host'],
        'port': config['database']['port']
    }
    
    conn = None

    @staticmethod
    def connect():
        """
        Establish a connection to the PostgreSQL database.
        """
        if db_utils.conn is None:
            try:
                db_utils.conn = psycopg2.connect(**db_utils.conn_params)
                db_utils.conn.autocommit = False  # Disable autocommit
                db_utils.logger.info("Database connection established.")
            except psycopg2.DatabaseError as error:
                db_utils.logger.error(f"Database connection error: {error}")

    @staticmethod
    def close():
        """
        Close the connection to the PostgreSQL database.
        """
        if db_utils.conn:
            db_utils.conn.close()
            db_utils.conn = None
            db_utils.logger.info("Database connection closed.")

    @staticmethod
    def commit():
        """
        Commit the current transaction.
        """
        if db_utils.conn:
            try:
                db_utils.conn.commit()
                db_utils.logger.info("Transaction committed.")
            except psycopg2.DatabaseError as error:
                db_utils.logger.error(f"Commit error: {error}")
                db_utils.conn.rollback()

    @staticmethod
    def rollback():
        """
        Rollback the current transaction.
        """
        if db_utils.conn:
            try:
                db_utils.conn.rollback()
                db_utils.logger.info("Transaction rolled back.")
            except psycopg2.DatabaseError as error:
                db_utils.logger.error(f"Rollback error: {error}")

    @staticmethod
    def create_db():
        """
        Create the PostgreSQL database and the necessary tables.
        """
        db_utils.connect()
        cur = db_utils.conn.cursor()

        try:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS stock_data (
                    id SERIAL PRIMARY KEY,
                    ticker TEXT NOT NULL,
                    date TIMESTAMP NOT NULL,
                    open REAL NOT NULL,
                    high REAL NOT NULL,
                    low REAL NOT NULL,
                    close REAL NOT NULL,
                    adj_close REAL NOT NULL,
                    volume REAL NOT NULL,
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

            db_utils.logger.info("Database tables created.")
        except psycopg2.DatabaseError as error:
            db_utils.logger.error(f"Error creating tables: {error}")
            db_utils.conn.rollback()
        finally:
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
        query = f"INSERT INTO {table}({cols}) VALUES ({','.join(['%s' for _ in range(len(df.columns) + 1)])}) ON CONFLICT(ticker, date) DO UPDATE SET "
        update_cols = ','.join([f"{col}=EXCLUDED.{col}" for col in list(df.columns)])
        query += update_cols

        cur = db_utils.conn.cursor()
        try:
            cur.executemany(query, tuples)
            db_utils.logger.info("Data inserted/updated successfully in the table.")
        except psycopg2.DatabaseError as error:
            db_utils.logger.error(f"Error: {error}")
            db_utils.conn.rollback()
        finally:
            cur.close()

    @staticmethod
    def get_ticker_from_stock():
        db_utils.connect()
        cur = db_utils.conn.cursor()
        
        try:
            # Query to select distinct tickers
            cur.execute('''
            SELECT DISTINCT ticker FROM stock_data
            ''')
            
            # Fetch all results
            rows = cur.fetchall()
            tickers = [row[0] for row in rows]
            return tickers
        except psycopg2.DatabaseError as error:
            db_utils.logger.error(f"Error: {error}")
            return []
        finally:
            cur.close()

    @staticmethod
    def get_data_from_db(ticker, start=None, end=None):
        """
        Retrieve historical stock data from the database.
        """
        db_utils.connect()
        try:
            cur = db_utils.conn.cursor()
            query = "SELECT date, open, high, low, close, adj_close, volume, dividends, stock_splits, capital_gains FROM stock_data WHERE ticker = %s"
            params = [ticker]
            if start:
                query += " AND date >= %s"
                params.append(start)
            if end:
                query += " AND date <= %s"
                params.append(end)
            cur.execute(query, params)
            data = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            df = pd.DataFrame(data, columns=columns)

            # Remove rows with NaN values
            df = df.dropna(axis=1, how='all')

            # Convert 'date' column to datetime format
            df['date'] = pd.to_datetime(df['date'])

            return df
        except psycopg2.DatabaseError as error:
            db_utils.logger.error(f"Error: {error}")
            return None
        finally:
            cur.close()

    @staticmethod
    def insert_listing_status(data):
        """
        Insert listing status data into the listing_status table.
        """
        db_utils.connect()
        cur = db_utils.conn.cursor()

        try:
            for index, row in data.iterrows():
                cur.execute('''
                    INSERT INTO listing_status (symbol, name, exchange, assetType, ipoDate, delistingDate, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (symbol) DO NOTHING
                ''', (
                    row['symbol'], row['name'], row['exchange'], row['assetType'],
                    row['ipoDate'], row['delistingDate'], row['status']
                ))

            db_utils.logger.info("Listing status data inserted successfully.")
        except psycopg2.DatabaseError as error:
            db_utils.logger.error(f"Error: {error}")
            db_utils.conn.rollback()
        finally:
            cur.close()

    @staticmethod
    def insert_wilshire_stocks(data):   
        db_utils.connect()
        cur = db_utils.conn.cursor()

        try:
            extras.execute_values(
                cur, 
                "INSERT INTO wilshire_5000 (Ticker, Name, Sector, Price, Dividend_Yield, One_Year_Dividend_Growth, Five_Year_Dividend_Growth_Annualized, Dividends_Per_Share, Market_Cap_M, Trailing_PE_Ratio, Payout_Ratio, Beta, Fifty_Two_Week_High, Fifty_Two_Week_Low) VALUES %s",
                [tuple(x) for x in data.to_numpy()]
            )
            db_utils.logger.info("Wilshire 5000 data inserted successfully.")
        except psycopg2.DatabaseError as error:
            db_utils.logger.error(f"Error: {error}")
            db_utils.conn.rollback()
        finally:
            cur.close()

    @staticmethod
    def get_wilshire_distinct_sectors():
        db_utils.connect()
        cur = db_utils.conn.cursor()
        
        try:
            # Query to select distinct sectors
            cur.execute('''
            SELECT DISTINCT Sector FROM wilshire_5000
            WHERE Sector IS NOT NULL
            ''')
            
            # Fetch all results
            rows = cur.fetchall()
            sectors = [row[0] for row in rows]
            return sectors
        except psycopg2.DatabaseError as error:
            db_utils.logger.error(f"Error: {error}")
            return []
        finally:
            cur.close()

    @staticmethod
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
        WHERE Sector = %s
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
            SELECT symbol FROM listing_status WHERE exchange = %s
        ''', (exchange,))

        exchange_tickers = [row[0] for row in cur.fetchall()]

        cur.close()
        return exchange_tickers