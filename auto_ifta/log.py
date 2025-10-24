from rich.logging import RichHandler

import logging
import os

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
FORMAT = "%(message)s"
LOGFILE_PATH = os.path.join(MODULE_DIR, "autoifta.log")


logging.basicConfig(
    level="INFO",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[
        RichHandler(),
        logging.FileHandler(LOGFILE_PATH, mode='a')]
)


log = logging.getLogger("rich")

