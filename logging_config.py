import logging
from logging.handlers import RotatingFileHandler
import os

LOG_NAME = "plant_app"

def setup_logging():
    # Путь до каталога логов рядом с файлом
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "app.log")

    logger = logging.getLogger(LOG_NAME)
    logger.setLevel(logging.INFO)

    # ВАЖНО: не добавлять хендлеры повторно
    if len(logger.handlers) == 0:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5_000_000,
            backupCount=5,
            encoding="utf-8"  # emojis supported
        )
        formatter = logging.Formatter(
            "%(asctime)s — %(levelname)s — %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Чтобы FastAPI/uvicorn не выводил ошибки
        logger.propagate = False

    return logger
