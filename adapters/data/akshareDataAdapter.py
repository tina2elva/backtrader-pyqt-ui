import akshare as ak
import efinance as ef
import pandas as pd
from pandas import DataFrame


def download_data(code,
                  start_date="20000101",
                  end_date="20201231",
                  adjust="qfq",
                  period="daily"):
    try:
        data = ak.stock_zh_a_hist(symbol=code, start_date=start_date, end_date=end_date, adjust=adjust,
                                  period=period)
    except KeyError:
        if adjust == "qfq":
            fqt = 1
        elif adjust == "hfq":
            fqt = 2

        if period == "daily":
            klt = 101
        elif period == "weekly":
            klt = 102
        elif period == "monthly":
            klt = 103
        data = ef.stock.get_quote_history(code, beg=start_date, end=end_date, fqt=fqt, klt=klt)
    if isinstance(data, type(None)) or data.empty:
        return DataFrame(columns=['datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])

    data.日期 = pd.to_datetime(data.日期)
    data = data[['日期', '开盘', '最高', '最低', '收盘', '成交量']]
    data.columns = ['datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
    data.set_index("datetime", drop=False, inplace=True)
    return data
