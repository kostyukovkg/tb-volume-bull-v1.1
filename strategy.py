import datetime
import time
from binance.client import Client
from utils import asset_list, df_download, trade_to_excel
import threading
from logger_config import logger

portfolio = list()
portfolio_lock = threading.Lock() # portfolio block

def strategy_buy():
    """
    Gets a list of coins from asset_list(), checks each coin to strategy criteria,
    adds to portfolio dictionary.
    :return: modified portfolio
    """
    while True:
        assets = asset_list()
        logger.debug(f"Possible tickers to buy: {assets}")
        logger.info(f"ℹ️ Number of possible tickers to buy: {len(assets)}")
        with portfolio_lock:
            for asset in assets:
                # check if asset is already in portfolio
                if asset not in [x['ticker'] for x in portfolio]:
                    logger.debug(f"Check ticker to buy: {asset}")
                    # if not - check if it fits the strategy and must be included into portfolio
                    df = df_download(asset, Client.KLINE_INTERVAL_1HOUR, 8)
                    if df is None or len(df)<6:
                        logger.warning(f'⚠️ Not enough data for {asset}, passed')
                        continue
                    try:
                        # strategy criteria
                        mean_volume = round(df['Volume'][:6].mean(), 4)
                        if df['Volume'].iloc[-2] > 3 * mean_volume and \
                            df['Volume'].iloc[-2] > 2 * df['Volume'].iloc[-3] and \
                            df['Volume'].iloc[-2] > 2 * df['Volume'].iloc[-4] and \
                            df['Close'].iloc[-2] > df['Close'].iloc[-3] and \
                            df['Close'].iloc[-2] > df['Close'].iloc[-4]:
                            new_asset = {
                                'ticker':asset,
                                'qty':float(),
                                'buy_price':float(),
                                'value':float(),
                                'profit': float(),
                                'stop_loss':float(),
                                'target':float(),
                                'current_price': float(),
                                'open':False
                            }
                            portfolio.append(new_asset)
                            logger.info(f"📥 ADD new asset {asset}")
                        else:
                            logger.info(f"{asset} does not fit strategy criteria to buy")
                    except IndexError as e:
                        logger.error(f"❗Error to buy {asset['ticker']: {e}}", exc_info=True)
                        continue
        logger.info(f"ℹ️ Current portfolio: {portfolio}")
        time.sleep(3600)


def buy(buy_amount):
    """
    Buys coins with no open position in portfolio dictionary.
    Modifies dictionary for each coin with buy and sell parameters.
    :param buy_amount: amount of USDT to buy a coin
    :return: modified portfolio
    """
    while True:
        with portfolio_lock:
            for asset in portfolio:
                if not asset['open']:
                    try:
                        logger.debug(f"Price check to buy {asset}")
                        df_asset = df_download(asset['ticker'], '1h', '480')
                        if df_asset is None:
                            continue
                        buy_price = round(df_asset['Close'].iloc[-1], 6)
                        qty = int(buy_amount / buy_price)
                        if qty <= 0:
                            logger.debug(f"{asset} quantity is <= 0")
                            continue
                        sl = round(buy_price * 0.985, 6)
                        target = round(buy_price * 1.02, 6)

                        asset['qty'] = qty
                        asset['buy_price'] = buy_price
                        asset['value'] = buy_price * qty
                        asset['stop_loss'] = sl
                        asset['target'] = target,
                        asset['current_price'] = 0
                        asset['profit'] = 0
                        asset['open'] = True
                        logger.info(f"✅ BUY {asset['ticker']} at price {buy_price}")
                        logger.debug(f"ℹ️ Portfolio after buy action: {portfolio}")

                        # write to trades.xlsx
                        trade_to_excel({
                            'Time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'Ticker': asset['ticker'],
                            'Side': 'BUY',
                            'Qty': qty,
                            'Price': buy_price,
                            'Value': buy_price * qty,
                            'Profit': 0
                        })
                    except Exception as e:
                        logger.error(f"❗Error to buy {asset['ticker']: {e}}", exc_info=True)
        time.sleep(5)


def sell():
    """
    Sells coins under specified target or stop loss params specified in a dictionary
    :return: modified portfolio
    """
    while True:
        with portfolio_lock:
            for i in range(len(portfolio)):
                asset = portfolio[i]
                if asset['open']:
                    try:
                        logger.debug(f"Price check to sell {asset}")
                        df_asset = df_download(asset['ticker'], '1h', '480')
                        if df_asset is None:
                            continue
                        current_price = round(df_asset['Close'].iloc[-1], 6)
                        if current_price < asset['stop_loss'] or current_price > asset['target']:
                            asset['profit'] = current_price * asset['qty'] - asset['value']
                            asset['open'] = False
                            portfolio.pop(i)
                            logger.info(f"💰SOLD {asset['ticker']} at price {current_price} | PROFIT: {asset['profit']:.6f}")
                            logger.debug(f"ℹ️ Portfolio after sell: {portfolio}")

                            trade_to_excel({
                                'Time': datetime.datetime.now().strftime(
                                    '%Y-%m-%d %H:%M:%S'),
                                'Ticker': asset['ticker'],
                                'Side': 'SELL',
                                'Qty': asset['qty'],
                                'Price': current_price,
                                'Value': current_price * asset['qty'],
                                "Profit": asset['profit']
                            })
                            break
                    except Exception as e:
                        logger.error(f"❗Error to sell {asset['ticker']: {e}}", exc_info=True)
        time.sleep(5)