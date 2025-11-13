import logging
from logging.handlers import RotatingFileHandler

# Create logger
logger = logging.getLogger("TextUploaderBot")
logger.setLevel(logging.ERROR)

# Formatter for logs
formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S"
)

# Rotating file handler (max 50MB, 10 backups)
file_handler = RotatingFileHandler("Assist.txt", maxBytes=50_000_000, backupCount=10)
file_handler.setFormatter(formatter)

# Stream handler (console output)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Reduce verbosity of pyrogram logs
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Usage example:
# logger.error("This is an error message")
# logger.info("This is an info message")
