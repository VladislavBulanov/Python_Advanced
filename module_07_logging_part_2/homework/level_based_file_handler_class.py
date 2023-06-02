"""A module with custom class for creating custom handler."""

import logging


class LevelBasedFileHandler(logging.Handler):
    """The class to create custom logging file handler,
    which writes logs in files depending on log level."""

    def __init__(
            self,
            debug_filename: str,
            info_filename: str,
            warning_filename: str,
            error_filename: str,
            critical_filename: str,
    ) -> None:
        """The class constructor."""

        super().__init__()
        self.__debug_filename = debug_filename
        self.__info_filename = info_filename
        self.__warning_filename = warning_filename
        self.__error_filename = error_filename
        self.__critical_filename = critical_filename

    def emit(self, record: logging.LogRecord) -> None:
        """
        This method is responsible for handling the log record
        and performing the desired action, such as writing to a file
        or sending over the network.
        :param record: the log record to be processed
        """

        if record.levelname == "DEBUG":
            with open(self.__debug_filename, 'a', encoding='utf-8') as file:
                file.write(f"{self.format(record)}\n")

        elif record.levelname == "INFO":
            with open(self.__info_filename, 'a', encoding='utf-8') as file:
                file.write(f"{self.format(record)}\n")

        elif record.levelname == "WARNING":
            with open(self.__warning_filename, 'a', encoding='utf-8') as file:
                file.write(f"{self.format(record)}\n")

        elif record.levelname == "ERROR":
            with open(self.__error_filename, 'a', encoding='utf-8') as file:
                file.write(f"{self.format(record)}\n")

        elif record.levelname == "CRITICAL":
            with open(self.__critical_filename, 'a', encoding='utf-8') as file:
                file.write(f"{self.format(record)}\n")
