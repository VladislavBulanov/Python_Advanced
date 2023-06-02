"""A module for config logger."""

import logging
import sys


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


def config_logger(src_logger: logging.Logger) -> logging.Logger:
    """
    The function receives source logger to configure
    him and returns modified version.
    :param src_logger: source logger to modify
    """

    src_logger.setLevel('DEBUG')

    stream_handler = logging.StreamHandler(stream=sys.stdout)
    file_handler = LevelBasedFileHandler(
        "calc_debug.log",
        "calc_info.log",
        "calc_warning.log",
        "calc_error.log",
        "calc_critical.log",
    )

    formatter = logging.Formatter(
        fmt="%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s",
        datefmt='%H:%M:%S',
    )

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    src_logger.addHandler(stream_handler)
    src_logger.addHandler(file_handler)

    return src_logger

    # # Or:
    # logging.basicConfig(
    #     level=logging.DEBUG,
    #     stream=sys.stdout,
    #     format="%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s",
    #     datefmt='%H:%M:%S',
    # )
    # return src_logger
