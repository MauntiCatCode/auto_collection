from rich.logging import RichHandler

import logging
import os

from config import MODULE_DIR

FORMAT = "%(message)s"
LOGFILE_PATH = os.path.join(MODULE_DIR, "autoemail.log")


logging.basicConfig(
    level="DEBUG",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[
        RichHandler(),
        logging.FileHandler(LOGFILE_PATH, mode='a')]
)


log = logging.getLogger("rich")

