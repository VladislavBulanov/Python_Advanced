import logging
import sys
from utils import string_to_operator


logger = logging.getLogger("app")


def config_logger() -> None:
    """The function configures logger settings via logging.basicConfig()."""

    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout,
        format="%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s",
        datefmt='%H:%M:%S',
    )

    # # Or:
    # logger.setLevel('DEBUG')
    # stream_handler = logging.StreamHandler(stream=sys.stdout)
    # formatter = logging.Formatter(
    #     fmt="%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s",
    #     datefmt='%H:%M:%S',
    # )
    # stream_handler.setFormatter(formatter)
    # logger.addHandler(stream_handler)


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


if __name__ == '__main__':
    config_logger()
    # calc(sys.argv[1:])
    calc([5, "*", 9])
