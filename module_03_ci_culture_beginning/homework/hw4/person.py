from datetime import datetime


class Person:
    """The class describing a person."""

    def __init__(self, name: str, birth_year: int, address: str = '') -> None:
        """
        The class constructor.
        :param name: name of person
        :param birth_year: year of person's birth
        :param address: address of person's home
        (empty string, if person is homeless)
        """
        if not name.isalpha() or not isinstance(name, str):
            raise ValueError('Введено некорректное имя')

        if not isinstance(birth_year, int):
            raise ValueError('Год рождения должен быть числом')

        if birth_year > datetime.now().year:
            raise ValueError('Год рождения не может быть больше текущего года')

        if not isinstance(address, str):
            raise ValueError('Адрес должен быть строкой')

        self.__name: str = name
        self.__birth_year: int = birth_year
        self.__address: str = address

    @property
    def name(self) -> str:
        """The getter of person's name."""
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """The setter of person's name."""
        if not name.isalpha() or not isinstance(name, str):
            raise ValueError('Введено некорректное имя')
        self.__name = name

    def get_age(self) -> int:
        """The function returns current age of person."""
        current_datetime = datetime.now()
        return current_datetime.year - self.__birth_year

    @property
    def address(self) -> str:
        """The getter of person's address."""
        return self.__address

    @address.setter
    def address(self, address: str) -> None:
        """The setter of person's address."""
        if not isinstance(address, str):
            raise ValueError('Адрес должен быть строкой')
        self.__address = address

    def is_homeless(self) -> bool:
        """
        The function checks if person is homeless.
        :return: True if person is homeless, False if he isn't
        """
        return len(self.__address) == 0
