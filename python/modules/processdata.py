import numpy as np 
import pandas as pd
from datetime import datetime # Import datetime class from datetime module

from db_sqlLite_utils import db_utils

class processdata:
    
    # We calculate a percentage rate of return for each day to compare investments.
    # Simple Rate of Return = (End Price - Beginning Price) / Beginning Price OR (EP / BP) - 1

    # Shift provides the value from the previous day
    # NaN is displayed because there was no previous day price for the 1st calculation
    @staticmethod
    def add_daily_return_to_df(df):
        df['daily_return'] = (df['adj_close'] / df['adj_close'].shift(1)) - 1
        return df 

    @staticmethod
    def get_return_defined_time(df, start_date, end_date):
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        return df.loc[mask]['daily_return'].sum()

    @staticmethod
    def get_roi_defined_time(df, start_date, end_date):
        df['date'] = pd.to_datetime(df['date'])
        start_val = df[df['date'] == start_date]['adj_close']
        print("Initial Price :", start_val)
        end_val = df[df['date'] == end_date]['adj_close']
        print("End Price :", end_val)
        # # Calculate return on investment
        roi = (end_val - start_val) / start_val
        # # Return the total return between 2 dates
        return start_val

    @staticmethod
    def formatDateDt(year, month, day):
        return datetime(year, month, day)
    
    @staticmethod
    def formatDateStr(year, month, day):
        return f"{year}-{month}-{day}"
    
    @staticmethod
    def get_valid_dates(df, sdate, edate):
        try:
            mask = (df['date'] > sdate) & (df['date'] <= edate) 
            sm_df = df.loc[mask]
            # Get smallest date that matches
            sm_date = sm_df['date'].iloc[0]
            last_date = sm_df['date'].iloc[-1]

            print(sm_date, " ", last_date)
        except Exception:
            print("Date Corrupted")
        else:
            return sm_date, last_date

    @staticmethod
    def get_roi_defined_time(df, start_date, end_date):
        start_val = df[df['date'] ==  start_date]['adj_close'].values[0]
        #print("Initial Price :", start_val)
        
        end_val = df[df['date'] == end_date]['adj_close'].values[0]
        #print("End Price :", end_val)

        # # Calculate return on investment
        roi = (end_val - start_val) / start_val
        return roi

    @staticmethod
    def get_mean_between_dates(df, sdate, edate):
        mask = (df['date'] > sdate) & (df['date'] <= edate)
        return df.loc[mask]["adj_close"].mean()

    @staticmethod
    def get_sd_between_dates(df, sdate, edate):
        mask = (df['date'] > sdate) & (df['date'] <= edate)
        return df.loc[mask]["adj_close"].std()

    @staticmethod
    def get_cov_between_dates(df, sdate, edate):
        mean = processdata.get_mean_between_dates(df, sdate, edate)
        sd = processdata.get_sd_between_dates(df, sdate, edate)
        return sd / mean

    @staticmethod
    def merge_df_by_column_name(col_name, sdate, edate, *tickers):
        # Will hold data for all dataframes with the same column name
        mult_df = pd.DataFrame()

        for x in tickers:
            print("Working on :", x)
            df = db_utils.get_data_from_db(x)
            df = processdata.add_daily_return_to_df(df)
            # Use a mask to grab data between defined dates
            mask = (df['date'] >= sdate) & (df['date'] <= edate)
            mult_df[x] = df.loc[mask][col_name].values
  
        return mult_df