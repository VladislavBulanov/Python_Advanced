"""A module for config logger."""

import logging  # for OOP config
# import sys  # for OOP config
#
# from level_based_file_handler_class import LevelBasedFileHandler  # for OOP config
#
#
# # Object-oriented programming configuration:
# def config_logger(src_logger: logging.Logger) -> logging.Logger:
#     """
#     The function receives source logger to configure
#     him and returns modified version.
#     :param src_logger: source logger to modify
#     """
#
#     src_logger.setLevel('DEBUG')
#
#     stream_handler = logging.StreamHandler(stream=sys.stdout)
#     file_handler = LevelBasedFileHandler(
#         "calc_debug.log",
#         "calc_info.log",
#         "calc_warning.log",
#         "calc_error.log",
#         "calc_critical.log",
#     )
#
#     formatter = logging.Formatter(
#         fmt="%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s",
#         datefmt='%H:%M:%S',
#     )
#
#     stream_handler.setFormatter(formatter)
#     file_handler.setFormatter(formatter)
#
#     src_logger.addHandler(stream_handler)
#     src_logger.addHandler(file_handler)
#
#     return src_logger
#
#     # # Or:
#     # logging.basicConfig(
#     #     level=logging.DEBUG,
#     #     stream=sys.stdout,
#     #     format="%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s",
#     #     datefmt='%H:%M:%S',
#     # )
#     # return src_logger


# Dict configuration:
dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s",
            "datefmt": '%H:%M:%S',
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "stream": "ext://sys.stdout",
        },
        "files_by_levels": {
            "class": "level_based_file_handler_class.LevelBasedFileHandler",
            "level": "DEBUG",
            "formatter": "base",
            "debug_filename": "calc_debug.log",
            "info_filename": "calc_info.log",
            "warning_filename": "calc_warning.log",
            "error_filename": "calc_error.log",
            "critical_filename": "calc_critical.log",
        },
        "timed_rotating_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "base",
            "filename": "utils.log",
            "when": "H",
            "interval": 10,
            "backupCount": 5,
        },

    },
    "loggers": {
        "app": {
            "level": "DEBUG",
            "handlers": ["console", "files_by_levels"],
        },
        "utils": {
            "level": "DEBUG",
            "handlers": ["console", "files_by_levels", "timed_rotating_file"],
        },
    },
}
