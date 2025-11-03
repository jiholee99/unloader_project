import logging
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

_loggers = {}  # cache to avoid re-creating handlers


def get_logger(name="app", log_subdir=None, level=logging.DEBUG):
    """
    Get or create a logger that writes to a dated log file inside its own folder.

    Args:
        name (str): Internal logger name (unique key).
        log_subdir (str, optional): Subdirectory name under logs/, e.g. 'image_processor'.
                                   If None, defaults to 'app'.
        level (int): Logging level (default: DEBUG).

    Returns:
        logging.Logger: Configured logger instance.
    """
    global _loggers

    # Reuse existing logger if already configured
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # --- log directory and file path ---
    subdir = log_subdir or name
    dir_path = os.path.join(LOG_DIR, subdir)
    os.makedirs(dir_path, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    log_path = os.path.join(dir_path, f"{date_str}.log")

    # --- file handler ---
    file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    file_handler.setFormatter(file_fmt)

    # --- console handler ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_fmt = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler.setFormatter(console_fmt)

    # --- attach handlers ---
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False
    _loggers[name] = logger
    return logger
