import logging
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

_loggers = {}  # cache to avoid re-creating handlers


def get_logger(name="app", log_subdir=None, level=logging.DEBUG):
    """
    Get or create a logger. Subdirectory affects only file path.
    Logger 'name' affects only how messages appear in logs.
    """
    global _loggers

    # Reuse existing logger if already configured
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # --- log directory ---
    # If no subdir provided -> logs/ directly OR logs/app/ (choose your style)
    if log_subdir:
        dir_path = os.path.join(LOG_DIR, log_subdir)
    else:
        dir_path = LOG_DIR  # store logs directly under logs/
        # OR: dir_path = os.path.join(LOG_DIR, "app")
    
    os.makedirs(dir_path, exist_ok=True)

    # --- log file ---
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
