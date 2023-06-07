"""A module with custom class for creating custom filter."""

import logging
import string


class AsciiFilter(logging.Filter):
    """A child class of logging.Filter class that checks
    if message of log record consists of ASCII-symbols only."""

    def filter(self, record: logging.LogRecord) -> bool:
        """
        :param record: the log record to be processed
        :return: True if message consists of ASCII-symbols only.
        False if it isn't
        """
        message = record.getMessage()
        if all(symbol in string.printable for symbol in message):
            return True
        return False
