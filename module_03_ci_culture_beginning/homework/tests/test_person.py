import unittest

from module_03_ci_culture_beginning.homework.hw4.person import Person


class TestClassPerson(unittest.TestCase):
    """The class for testing class 'Person'
    which describes a person and his properties."""

    @classmethod
    def setUpClass(cls) -> None:
        """Creates test instance of 'Person' class."""
        cls.test_person = Person('Vladi', 1995, 'Moscow')

    def test_can_create_instance_with_valid_args(self) -> None:
        """Positive test: the function checks if user can
        create class' instance with valid arguments."""
        Person('Name', 2000, 'City')

    def test_cannot_create_instance_with_invalid_name(self) -> None:
        """Negative test: the function checks
        if program raises error if name is invalid."""
        with self.assertRaises(ValueError):
            Person('Name1', 2000)

    def test_cannot_create_instance_with_future_birth_year(self) -> None:
        """Negative test: the function checks if program
        raises error if birth year is more than current year."""
        with self.assertRaises(ValueError):
            Person('Name', 2072)

    def test_cannot_create_instance_with_not_digital_year(self) -> None:
        """Negative test: the function checks
        if program raises error if birth year is string."""
        with self.assertRaises(ValueError):
            Person('Name', 'year')

    def test_cannot_create_instance_with_invalid_address(self) -> None:
        """Negative test: the function checks
        if program raises error if address is not string."""
        with self.assertRaises(ValueError):
            Person('Name', 2000, 101000)

    def test_can_get_name(self) -> None:
        """Positive test: the function checks
        if user can get person's name."""
        self.assertEqual(self.test_person.name, 'Vladi')

    def test_can_set_valid_name(self) -> None:
        """Positive test: the function checks
        if user can set valid name for class' instance."""
        man = Person('Name', 2000)
        man.name = 'Ivan'
        self.assertEqual(man.name, 'Ivan')

    def test_cannot_set_invalid_name(self) -> None:
        """Negative test: the function checks if program raises
        error if user tries set invalid name via setter."""
        with self.assertRaises(Exception):
            self.test_person.name = 123

    def test_can_get_age(self) -> None:
        """Positive test: the function checks
        if user can get person's age (test is valid for 2023)."""
        self.assertEqual(self.test_person.get_age(), 28)

    def test_can_get_address(self) -> None:
        """Positive test: the function checks
        if user can get person's address."""
        self.assertEqual(self.test_person.address, 'Moscow')

    def test_can_set_valid_address(self) -> None:
        """Positive test: the function checks
        if user can set valid person's address."""
        man = Person('Name', 2000)
        man.address = 'St. Petersburg'
        self.assertEqual(man.address, 'St. Petersburg')

    def test_cannot_set_invalid_address(self) -> None:
        """Negative test: the function checks
        if program raises error if address is invalid."""
        with self.assertRaises(ValueError):
            self.test_person.address = 123

    def test_can_get_homeless_true(self) -> None:
        """Positive test: the function checks if user
        can receive True if person is homeless."""
        man = Person('Name', 2000)
        self.assertTrue(man.is_homeless())

    def test_can_get_homeless_false(self) -> None:
        """Positive test: the function checks if user
        can receive False if person has home address."""
        self.assertTrue(not self.test_person.is_homeless())


if __name__ == '__main__':
    unittest.main()
