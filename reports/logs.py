import logging
import time
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)+19800s %(levelname)s %(name)s: %(lineno)s %(message)s', time.strftime("%b %d %Y %H:%M:%S"))
handler.setFormatter(formatter)
logger.addHandler(handler)
