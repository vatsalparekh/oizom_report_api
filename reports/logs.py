import logging
import time
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)+19800s  %(name)s - %(levelname)s - %(message)s',time.strftime("%b %d %Y %H:%M:%S"))
handler.setFormatter(formatter)
logger.addHandler(handler)
