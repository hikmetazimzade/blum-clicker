import logging


class ColoredFormatter(logging.Formatter):
    """
    A custom logging formatter that adds color to log messages based on their severity level.

    The log messages are colorized according to their log level to improve readability
    in the terminal. It applies ANSI escape codes to format the message with different colors.

    Attributes:
        COLORS (dict): A dictionary that maps log levels (INFO, WARNING, ERROR, DEBUG)
                       to their corresponding ANSI color codes.
    """

    COLORS = {
        'INFO': '\033[97m',  # White
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',  # Red
        'DEBUG': '\033[94m',  # Blue
        'RESET': '\033[0m',  # Reset to default
    }

    def format(self, record):
        """
        Overrides the `format` method to add color to log messages.

        The method checks the log level of the `record` and applies the corresponding
        ANSI color code. After formatting the log message, it resets the color to
        the default terminal color.

        Args:
            record (LogRecord): The log record object that contains all the information
                                related to the log message (e.g., level, message, etc.).

        Returns:
            str: The formatted log message with applied color.
        """
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        return f"{color}{super().format(record)}{reset}"


def get_logger():
    """
    Creates and configures a logger instance for the BlumClicker application.

    This logger outputs log messages to the console with color formatting based
    on the log level. The logger uses the `ColoredFormatter` to apply colors
    for different severity levels (INFO, WARNING, ERROR, DEBUG).

    Returns:
        Logger: A logger instance configured with colored output and set to the DEBUG level.
    """
    logger = logging.getLogger('BlumClicker')

    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()

        formatter = ColoredFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger