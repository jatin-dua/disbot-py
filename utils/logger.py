import logging


def setup_logging(*, func: str) -> logging.Logger:
    logger = logging.getLogger(func)
    logger.setLevel(logging.DEBUG)

    log_format = "%(asctime)s [%(levelname)s] %(module)s - %(funcName)s: %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S %p"

    formatter = logging.Formatter(
        fmt=log_format,
        datefmt=date_format,
    )

    # Log to files
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
