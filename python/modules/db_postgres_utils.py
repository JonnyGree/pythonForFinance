import pandas as pd
import psycopg2
from psycopg2 import extras
import logging
import configparser

class db_utils:
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
        
    """
    Example usage:
    Call the function for bulk insert
    db_utils.execute_values(df, 'table_name', 'ticker')

    Don't forget to close the connection when done:
    db_utils.conn.close()   
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
        cursor = db_utils.conn.cursor()
        try:
            extras.execute_values(cursor, query, tuples)
            db_utils.conn.commit()
            db_utils.logger.info("execute_values() done")
        except (Exception, psycopg2.DatabaseError) as error:
            db_utils.logger.error("Error: %s", error)
            db_utils.conn.rollback()
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
            cursor = db_utils.conn.cursor()
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
            db_utils.logger.error("Error: %s", error)
            return None
