import logging


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s\n\n', level=logging.DEBUG)
logger = logging.getLogger(__name__)