import logging.config
import logging_tree
import sys
from utils import string_to_operator

# from logging_config import config_logger  # for OOP config
from logging_config import dict_config


# logger = config_logger(logging.getLogger("app"))  # for OOP config
logger = logging.getLogger("app")
logging.config.dictConfig(dict_config)


def calc(args):
    logger.debug(f"Arguments: {args}")

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.error("Error while converting number 1")
        logger.error(e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.error("Error while converting number 2")
        logger.error(e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    logger.debug(f"Result: {result}")
    logger.info(f"{num_1} {operator} {num_2} = {result}")


def get_logging_tree() -> None:
    """The function records logging tree in
    txt-file using logging_tree library."""

    with open('logging_tree.txt', 'w', encoding='utf-8') as file:
        sys.stdout = file
        logging_tree.printout()
        sys.stdout = sys.__stdout__
        # # Or:
        # file.write(logging_tree.format.build_description())


if __name__ == '__main__':
    get_logging_tree()
    calc(sys.argv[1:])
