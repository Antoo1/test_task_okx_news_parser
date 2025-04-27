import logging


def setup_logger():
    formatter = logging.Formatter(
        fmt='%(levelname)s::%(asctime)s:%(name)s.%(funcName)s\n%(message)s\n',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger


logger: logging.Logger = setup_logger()
