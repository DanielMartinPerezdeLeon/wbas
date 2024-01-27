import logging
import os.path
from datetime import datetime
import config

# Define colors for different log levels
LOG_COLORS = {
    logging.DEBUG: '\033[92m',  # Green
    logging.INFO: '\033[94m',  # Blue
    logging.WARNING: '\033[93m',  # Yellow
    logging.ERROR: '\033[91m',  # Red
    logging.CRITICAL: '\033[95m'  # Purple
}

# Reset color
RESET_COLOR = '\033[0m'


# Custom formatter to include colors
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_color = LOG_COLORS.get(record.levelno, RESET_COLOR)
        log_message = super().format(record)
        return f"{log_color}{log_message}{RESET_COLOR}"


# Configure logging
logging.basicConfig(level=config.logging_level,  # Set the logging level
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=os.path.join(os.path.dirname(__file__), '..', 'logs',
                                          f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'))
                    # Define log message format

# Create a handler and set formatter
console_handler = logging.StreamHandler()
console_formatter = ColoredFormatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Add handler to the root logger
logging.getLogger('').addHandler(console_handler)

logger = logging.getLogger(__name__)
