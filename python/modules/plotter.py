import matplotlib.pyplot as plt
# from db_sqlLite_utils import db_utils

class pl:
    
    @staticmethod
    def plot_closing_prices(data, ticker):
        plt.figure(figsize=(10, 5))
        plt.plot(data['date'], data['close'], label='Closing Price')
        plt.title(f'{ticker} Closing Prices')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend()
        plt.show()

    # @staticmethod
    # def plot_closing_prices_from_db(ticker, start=None, end=None):
    #     """
    #     Plot closing prices over time.
    #     """
    #     data_df, _ = db_utils.get_data_from_db(ticker, start, end)
    #     if data_df is not None:
    #         plt.figure(figsize=(10, 5))
    #         plt.plot(data_df['date'], data_df['close'], label='Closing Price')
    #         plt.title(f'{ticker} Closing Prices')
    #         plt.xlabel('Date')
    #         plt.ylabel('Close Price')
    #         plt.legend()
    #         plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    #         plt.tight_layout()  # Adjust layout to prevent clipping of labels
    #         plt.show()