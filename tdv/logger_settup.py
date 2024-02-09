import logging
from datetime import datetime

"""Change to include values in outputs"""

timestamp_format = '%Y-%m-%d_%H-%M-%S'
current_timestamp = datetime.now().strftime(timestamp_format)
log_filename = f'app_{current_timestamp}.log'
LOG_FORMAT = "%(asctime)s - %(levelname)s: %(message)s"

file_handler = logging.FileHandler(log_filename, 'w')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S'))

# Configure logging to print to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S'))

# Get the root logger and add both handlers to it
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# This version bellow will not output log in terminal
# import logging
# from datetime import datetime
#
# """Change to include values in outputs"""
#
# timestamp_format = '%Y-%m-%d_%H-%M-%S'
# current_timestamp = datetime.now().strftime(timestamp_format)
# log_filename = f'app_{current_timestamp}.log'
#
# LOG_FORMAT = "%(asctime)s - %(levelname)s: %(message)s"
# logging.basicConfig(filename=log_filename, filemode='w', format=LOG_FORMAT, level=logging.INFO,
#                     datefmt='%Y-%m-%d %H:%M:%S')
# logger = logging.getLogger(__name__)

