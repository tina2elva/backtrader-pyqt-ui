from utils import const
from utils.utils import save_dataframe_to_csv, read_from_csv


def get_data(code,
             start_date="20000101",
             end_date="20201231",
             adjust="qfq",
             period="daily",
             refresh=True):

    if not refresh:
        stock_data = read_from_csv(code, start_date, end_date)
        if not stock_data.empty:
            return stock_data
    if const.DATA_FROM == "akshare":
        from adapters.data.akshareDataAdapter import download_data
    elif const.DATA_FROM == "tushare":
        from adapters.data.tushareDataAdapter import download_data
        mark = get_stock_market(code)
        code = code + "." + mark.upper()
    elif const.DATA_FROM == "mootdx":
        from adapters.data.mootdxDataAdapter import download_data
    else:
        raise Exception("const.DATA_FROM is wrong")
    stock_data = download_data(code, start_date, end_date, adjust, period)
    if not stock_data.empty:
        save_dataframe_to_csv(stock_data, code)
    return stock_data


def get_stock_market(symbol=""):
    """判断股票ID对应的证券市场匹配规则

    ['50', '51', '60', '90', '110'] 为 sh
    ['00', '12'，'13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 sz
    ['5', '6', '9'] 开头的为 sh， 其余为 sz

    :param string: False 返回市场ID，否则市场缩写名称
    :param symbol: 股票ID, 若以 'sz', 'sh' 开头直接返回对应类型，否则使用内置规则判断
    :return 'sh' or 'sz'
    """

    assert isinstance(symbol, str), "stock code need str type"

    market = "sh"

    if symbol.startswith(("sh", "sz", "SH", "SZ")):
        market = symbol[:2].lower()

    elif symbol.startswith(("50", "51", "60", "68", "90", "110", "113", "132", "204")):
        market = "sh"

    elif symbol.startswith(("00", "12", "13", "18", "15", "16", "18", "20", "30", "39", "115", "1318")):
        market = "sz"

    elif symbol.startswith(("5", "6", "9", "7")):
        market = "sh"

    elif symbol.startswith(("4", "8")):
        market = "bj"
    return market
