import time, threading, os
from client import get_client
import pandas as pd
from logger_config import logger

os.makedirs('logs', exist_ok=True)
trade_log_lock = threading.Lock()
COLUMNS = ['Time', 'Ticker', 'Side', 'Qty', 'Price', 'Value', 'Profit']
def trade_to_excel(trade_data):
    """
    Function that adds new row to excel 'trades' file with coin trade data that was bought or sold
    :param trade_data: coin trade data to add in Excel
    :return: adds new data to excel
    """
    file_path = 'trades.xlsx'

    with trade_log_lock:
        new_row = pd.DataFrame([trade_data], columns=COLUMNS)

        if not os.path.exists(file_path):
            new_row.to_excel(file_path, index=False)
        else:
            df_existing = pd.read_excel('trades.xlsx')
            df_new = pd.DataFrame([trade_data])
            df_updated = pd.concat([df_existing, df_new], ignore_index=True)
            df_updated.to_excel('trades.xlsx', index=False)


def df_download(coin, interval, lookback):
    """
    Loads a dataframe of a coin (ticker) candle interval for a specified period (lookback)
    :param coin: ticker of a crypto coin
    :param interval: candle interval
    :param lookback: lookback period for a given candle interval
    :return: filtered pd.DataFrame
    """
    time.sleep(1)
    try:
        logger.debug(f"📊 Data download for {coin}")
        # load frame for a coin with trade data
        frame = pd.DataFrame(get_client().get_historical_klines(coin, interval, limit=lookback))
        if len(frame)>0:
            frame.columns = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume',
                            'CloseTime', 'QuoteAssetVolume', 'NumberOfTrades',
                            'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume',
                            'Ignore']
            frame = frame.set_index('OpenTime')
            frame.index = pd.to_datetime(frame.index, unit = 'ms')
            frame = frame.astype(float)
            frame = frame.iloc[:,:6]
            return frame
        else:
            logger.warning(f"🟡 No data for {coin}")
    except Exception as e:
        logger.error(f"❗ Error download data for {coin}: {e}")
        return None


def asset_list():
    """
    Gets a list of coins that are traded only to USDT and have grown by more than X% over the past day
    :return:list of coins
    """
    top_coins = []
    while not top_coins:
        try:
            logger.debug(f"📊 Data download for {top_coins}")
            all_tickers = pd.DataFrame(get_client().get_ticker())
        except Exception as e:
            logger.error(f"❗ Error download data for {top_coins}: {e}")
            continue
        # find USDT traded coins
        usdt = all_tickers[all_tickers.symbol.str.contains('USDT')]
        # delete irrelevant coins
        work = usdt[~((usdt.symbol.str.contains('UP')) | (
            usdt.symbol.str.contains("DOWN")))]
        work['priceChangePercent'] = work['priceChangePercent'].astype(float)
        work['symbol'] = work['symbol'].astype(str)
        # add to list only coins with > 5% daily growth
        work = work[work['priceChangePercent'] > 3]
        work = work['symbol']
        for ticker in work:
            if ticker[-4:] == 'USDT':
                top_coins.append(ticker)
    return top_coins
