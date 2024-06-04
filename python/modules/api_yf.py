import yfinance as yf
import pandas as pd
import logging

class api_yf:
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)  # Set logging level to INFO by default

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
            api_yf.logger.error("Error retrieving data from yf: %s", str(e))
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

            # Convert 'date' column to datetime format
            data['date'] = pd.to_datetime(data['date'])

            return data
        except Exception as e:
            api_yf.logger.error("Error retrieving data from yf: %s", str(e))
            return None
        