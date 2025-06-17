import logging
import os

# create logs dir
os.makedirs('logs', exist_ok=True)

# logs format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(module)s] %(message)s')

# set up console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# set up file writer
file_handler = logging.FileHandler('logs/bot.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# main logger
logger = logging.getLogger(())
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)
logger.addHandler(file_handler)