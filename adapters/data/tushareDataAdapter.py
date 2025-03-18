import json
import tushare as ts
import pandas as pd
from pandas import DataFrame


def download_data(code,
                  start_date="20000101",
                  end_date="20201231",
                  adjust="qfq",
                  period="daily"):
    with open(r'Datas/tushare_token.json', 'r') as load_json:
        token_json = json.load(load_json)
    token = token_json['token']
    ts.set_token(token)
    ts.pro_api(token)
    df = ts.pro_bar(ts_code=code, adj=adjust, start_date=start_date, end_date=end_date)
    if isinstance(df, type(None)) or df.empty:
        return DataFrame(columns=['datetime',  'Open', 'High', 'Low', 'Close', 'Volume'])
    df.trade_date = pd.to_datetime(df.trade_date)
    df = df[['trade_date', 'open', 'high', 'low', 'close', 'vol']]
    df.columns = ['datetime',  'Open', 'High', 'Low', 'Close', 'Volume']
    df.set_index("datetime", drop=False, inplace=True)
    df.fillna(0.0, inplace=True)
    df=df.iloc[::-1]  #反序
    return df
