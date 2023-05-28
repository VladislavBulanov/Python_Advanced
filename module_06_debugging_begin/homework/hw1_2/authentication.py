import getpass
import hashlib
import logging
import os
from re import findall
from typing import Set


logger = logging.getLogger("password_checker")

with open(os.path.abspath('/usr/share/dict/words'), 'r') as file:
    word_list: Set[str] = {
        word.strip().lower() for word in file if len(word.strip()) > 4
    }


def is_strong_password(password: str) -> bool:
    """
    The function checks if password is strong.
    :param password: the password that user inputted
    :return: True if password is strong, False if password is weak
    """

    password = password.lower()
    words = findall(r'[a-zA-Z]{5,}', password)

    for word in words:
        if word in word_list:
            return False

    return True


def input_and_check_password() -> bool:
    """
    The function requests password from user and verifies it.
    :return: True if password is valid, False if it doesn't
    """

    logger.debug("Начало input_and_check_password")
    password: str = getpass.getpass("Enter password: ")

    if not password:
        logger.warning("Вы ввели пустой пароль.")
        return False

    elif not is_strong_password(password):
        logger.warning("Вы ввели слишком слабый пароль")
        return False

    try:
        hasher = hashlib.md5()

        hasher.update(password.encode("latin-1"))

        if hasher.hexdigest() == "098f6bcd4621d373cade4e832627b4f6":
            return True

    except ValueError as error:
        logger.exception("Вы ввели некорректный символ ", exc_info=error)

    return False


if __name__ == "__main__":
    logging.basicConfig(filename='stderr.txt',
                        filemode='a',
                        format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")
    count_number: int = 3

    while count_number > 0:
        logger.info(f"У вас есть {count_number} попытки(-ок)")
        if input_and_check_password():
            exit(0)
        count_number -= 1

    logger.error("Пользователь трижды ввёл неправильный пароль!")
    exit(1)
