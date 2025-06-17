import threading, time
from strategy import strategy_buy, buy, sell, portfolio
from logger_config import logger


logger.info(f'✅ BOT STARTED. Current portfolio: {portfolio}')

if __name__ == '__main__':
    # initiate and start 3 threads: 'strategy_buy' runs every hour to check new trading data for coins
    # 'buy/sell' runs every 5 sec to check prices.
    thread_add = threading.Thread(target=strategy_buy, daemon=True)
    thread_buy = threading.Thread(target=buy, daemon=True, args=(100,))
    thread_sell = threading.Thread(target=sell, daemon=True)

    thread_add.start()
    thread_buy.start()
    thread_sell.start()

    # catches if user enters Ctrl+C
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.critical(f"❗Interrupted by user")