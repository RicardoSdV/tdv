import logging

"""Change to include values in outputs"""

LOG_FORMAT = "%(message)s"
logging.basicConfig(filename='app.log', filemode='w', format=LOG_FORMAT, level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
tdv_logger = logging.getLogger(__name__)

# Test
