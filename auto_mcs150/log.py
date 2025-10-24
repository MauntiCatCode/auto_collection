from rich.logging import RichHandler

import logging
import os

from config import MODULE_DIR


FORMAT = "%(message)s"
LOGFILE_PATH = os.path.join(MODULE_DIR, "auto_mcs150.log")

logging.basicConfig(
    level="INFO",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[
        RichHandler(),
        logging.FileHandler(LOGFILE_PATH, mode='a')
    ]
)

log = logging.getLogger("rich")

