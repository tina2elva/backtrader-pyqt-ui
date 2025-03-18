import os
from functools import wraps

import pandas as pd
import datetime


def save_dataframe_to_csv(df, code):
    stockfile = "./datas/ " + code + ".csv"
    if os.path.exists(stockfile):
        os.remove(stockfile)
    df.to_csv(stockfile)


def read_from_csv(code, start_date, end_date):
    stockfile = "./datas/ " + code + ".csv"
    if os.path.exists(stockfile):
        stock_data = pd.read_csv(stockfile)
        stock_data.datetime = pd.to_datetime(stock_data.datetime)
        stock_data.set_index("datetime", drop=False, inplace=True)
        # stock_data = stock_data.loc[start_date:datetime.datetime(end_date) + datetime.timedelta(days = 1), :]
        end_date = datetime.datetime.strptime(end_date, "%Y%m%d") + datetime.timedelta(days=1)
        start_date = datetime.datetime.strptime(start_date, "%Y%m%d")
        stock_data = stock_data.loc[start_date:end_date, :]
        return stock_data
    return pd.DataFrame()
