import time

from binance.client import Client
from logger_config import logger
import os

def get_client():
    """
    Client's entry point to Binance API
    :return: client profile
    """
    try:
        api_key = os.getenv("MY_KEY")
        api_secret = os.getenv("MY_PASS")
        client = Client(api_key, api_secret)
        logger.debug("Client Binance initiated")
        return client
    except Exception as e:
        logger.critical(f"❗Error to create Binance client: {e}", exc_info=True)
        time.sleep(10)
        get_client()
