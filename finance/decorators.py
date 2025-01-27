import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(messages)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def dec_log(func):
    def wrapper(*args, **kwargs):
        logger.info(f"Running {func.__name__} with args: {args}, kwargs: {kwargs}")
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            raise e

    return wrapper
