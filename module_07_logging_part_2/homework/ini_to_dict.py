"""A ini-file converted to dict-configuration."""

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "fileFormatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%Z",
        },
        "consoleFormatter": {
            "format": "%(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%Z",
        },
    },
    "handlers": {
        "consoleHandler": {
            "class": "StreamHandler",
            "level": "WARNING",
            "formatter": "consoleFormatter",
            "stream": "ext://sys.stdout",
        },
        "fileHandler": {
            "class": "FileHandler",
            "level": "DEBUG",
            "formatter": "fileFormatter",
            "filename": "logfile.log",
        },
    },
    "loggers": {
        "root": {
            "level": "DEBUG",
            "handlers": ["consoleHandler"],
        },
        "appLogger": {
            "level": "DEBUG",
            "handlers": ["consoleHandler", "fileHandler"],
            "qualname": "appLogger",
            "propagate": False,
        },
    },
}
