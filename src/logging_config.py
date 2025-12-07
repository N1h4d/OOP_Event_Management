import logging
from pathlib import Path

LOG_FILE = Path("logs/app.log")
LOG_FILE.parent.mkdir(exist_ok=True)

def setup_logging():
    # Root logger-i götür
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Köhnə handler-ləri tam sil
    if logger.handlers:
        logger.handlers.clear()

    # Yalnız FILE handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
