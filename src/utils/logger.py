import logging
import sys


def setup_logger(name: str = "httpbin_tests", level: int = logging.INFO) -> logging.Logger:
    """Setup and configure logger"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
        logger.addHandler(console_handler)
    logger.setLevel(level)
    return logger
