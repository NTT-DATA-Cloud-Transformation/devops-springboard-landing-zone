import logging
def configure_logging(log_level):
    """
    to set the logging level
    :param log_level:
    :return:
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)

    logging.basicConfig(level = numeric_level)


configure_logging("DEBUG")
