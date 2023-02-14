import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="{asctime} {levelname: <8} {message}",
    style= '{',
    filename= './app/logging/background.log',
    filemode= 'a'
)

logger = logging.getLogger(__name__)

# logger.info("This is an informational message.")
# logger.warning("This is a warning message.")
# logger.error("This is an error message.")