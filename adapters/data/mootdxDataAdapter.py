from mootdx.reader import Reader
from mootdx.quotes import Quotes
from mootdx.utils.adjust import to_adjust
import datetime
import pandas as pd

from utils import const


def download_data(code,
                  start_date="20000101",
                  end_date="20201231",
                  adjust="qfq",
                  period="daily"):
    reader = Reader.factory(market="std", tdxdir=const.TDX_DIR)
    df = reader.daily(code)
    df.insert(0,'code', code)
    df = to_adjust(df, code, adjust)
    end_date = datetime.datetime.strptime(end_date, "%Y%m%d") + datetime.timedelta(days=1)
    start_date = datetime.datetime.strptime(start_date, "%Y%m%d")
    df = df.loc[start_date:end_date, :]
    #df.datetime = pd.to_datetime(df.index)
    df['datetime'] = df.index
    df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
    df.columns = ['datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
    df.set_index("datetime", drop=False, inplace=True)
    return df
