import yfinance as yf
import pandas as pd
import psycopg2
from psycopg2 import extras
import logging
import configparser

class py4f_utils:
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)  # Set logging level to INFO by default

    config = configparser.ConfigParser()
    config.read('config.ini')

    conn_params = {
        'dbname': config['database']['dbname'],
        'user': config['database']['user'],
        'password': config['database']['password'],
        'host': config['database']['host'],
        'port': config['database']['port']
    }
    
    # Database connection
    conn = psycopg2.connect(**conn_params)

    @staticmethod
    def getDataFromYf(ticker, start=None, end=None):
        """
        Retrieve historical stock data from Yahoo Finance.
        
        Args:
        ticker (str): Ticker symbol of the stock.
        start (str): Start date in 'YYYY-MM-DD' format (optional).
        end (str): End date in 'YYYY-MM-DD' format (optional).
        
        Returns:
        DataFrame: Historical stock data.
        """
        try:
            if start is None and end is None:
                # If start and end dates are not provided, retrieve data for maximum period
                data = yf.download(ticker, period="max")

            else:
                # If start and/or end dates are provided, retrieve data for specified period
                data = yf.download(ticker, start=start, end=end)
            
            data = data.reset_index()
            data.index = data.index.tz_localize(None)
            data.rename(columns={'Capital Gains': 'Capital_Gains'}, inplace=True)
            data.rename(columns={'Stock Splits': 'Stock_Splits'}, inplace=True)
            data.rename(columns={'Adj Close': 'adj_close'}, inplace=True)
            data.columns = [col.lower() for col in data.columns]
            return data
        except Exception as e:
            py4f_utils.logger.error("Error retrieving data from yf: %s", str(e))
            return None

    @staticmethod
    def getFullDataFromYf(ticker, start=None, end=None):
        """
        Combine download    -> Open      High       Low     Close  Volume   Adj Close
        and     history     -> Open      High       Low     Close  Volume   Dividends  Stock Splits Capital Gain
        """
        try:
            if start is None and end is None:
                # If start and end dates are not provided, retrieve data for maximum period
                data_dw = yf.download(ticker, period="max")
                tick = yf.Ticker(ticker)
                data_hys = tick.history(period="max")

            else:
                # If start and/or end dates are provided, retrieve data for specified period
                data_dw = yf.download(ticker, start=start, end=end)
                tick = yf.Ticker(ticker)
                data_hys = tick.history(start=start, end=end)

            data_dw.index = data_dw.index.tz_localize(None)
            data_hys.index = data_hys.index.tz_localize(None)
            data = pd.concat([data_dw, data_hys[['Dividends', 'Stock Splits']]], axis=1)
           
            data = data.reset_index()
            data.rename(columns={'Capital Gains': 'Capital_Gains'}, inplace=True)
            data.rename(columns={'Stock Splits': 'Stock_Splits'}, inplace=True)
            data.rename(columns={'Adj Close': 'adj_close'}, inplace=True)
            data.columns = [col.lower() for col in data.columns]
            return data
        except Exception as e:
            py4f_utils.logger.error("Error retrieving data from yf: %s", str(e))
            return None
        
    """
    Example usage:
    Call the function for bulk insert
    py4f_utils.execute_values(df, 'table_name', 'ticker')

    Don't forget to close the connection when done:
    py4f_utils.conn.close()   
    """
    @staticmethod
    def execute_values(df, table, ticker):
        """
        Using psycopg2.extras.execute_values() to insert or update the dataframe
        """
        # Create a list of tuples from the dataframe values
        tuples = [tuple([ticker] + list(x)) for x in df.to_numpy()]
        # Comma-separated dataframe columns
        cols = 'ticker,' + ','.join(list(df.columns))
        # SQL query to execute
        query  = f"INSERT INTO {table}({cols}) VALUES %s ON CONFLICT (ticker, date) DO UPDATE SET "
        update_cols = ','.join([f"{col}=EXCLUDED.{col}" for col in list(df.columns)[1:]])
        query += update_cols
        cursor = py4f_utils.conn.cursor()
        try:
            extras.execute_values(cursor, query, tuples)
            py4f_utils.conn.commit()
            py4f_utils.logger.info("execute_values() done")
        except (Exception, psycopg2.DatabaseError) as error:
            py4f_utils.logger.error("Error: %s", error)
            py4f_utils.conn.rollback()
            cursor.close()
            return 1
        cursor.close()

    @staticmethod
    def getDataFromDb(ticker, start=None, end=None):
        """
        Retrieve historical stock data from the database.
        
        Args:
        ticker (str): Ticker symbol of the stock.
        start (str): Start date in 'YYYY-MM-DD' format (optional).
        end (str): End date in 'YYYY-MM-DD' format (optional).
        
        Returns:
        DataFrame: Historical stock data if successful, None otherwise.
        """
        try:
            cursor = py4f_utils.conn.cursor()
            query = f"SELECT * FROM stock_data WHERE ticker = %s"
            params = [ticker]
            if start:
                query += " AND date >= %s"
                params.append(start)
            if end:
                query += " AND date <= %s"
                params.append(end)
            cursor.execute(query, params)
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(data, columns=columns)
            cursor.close()
            return df
        except (Exception, psycopg2.DatabaseError) as error:
            py4f_utils.logger.error("Error: %s", error)
            return None
