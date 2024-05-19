import platform

platform = platform.system()


def throw_unsupported_os_error():
    raise Exception("This type of OS is not supported.")


# Import logging system
if platform == 'Windows':
    import logging

    # Configure logging for Windows
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
elif platform == "Linux":
    import syslog
else:
    throw_unsupported_os_error()


def log_info(message):
    if platform == 'Windows':
        logging.info(message)
    elif platform == "Linux":
        syslog.syslog(syslog.LOG_INFO, message)
    else:
        throw_unsupported_os_error()


def log_debug(message):
    if platform == 'Windows':
        logging.debug(message)
    elif platform == "Linux":
        syslog.syslog(syslog.LOG_DEBUG, message)
    else:
        throw_unsupported_os_error()


def log_warning(message):
    if platform == 'Windows':
        logging.warning(message)
    elif platform == "Linux":
        syslog.syslog(syslog.LOG_WARNING, message)
    else:
        throw_unsupported_os_error()


def log_error(message):
    if platform == 'Windows':
        logging.error(message)
    elif platform == "Linux":
        syslog.syslog(syslog.LOG_ERR, message)
    else:
        throw_unsupported_os_error()


def log_critical(message):
    if platform == 'Windows':
        logging.critical(message)
    elif platform == "Linux":
        syslog.syslog(syslog.LOG_CRIT, message)
    else:
        throw_unsupported_os_error()
