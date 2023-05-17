import unittest
from freezegun import freeze_time

from module_03_ci_culture_beginning.homework.hw1.hello_word_with_day import app


class TestHelloWorldApp(unittest.TestCase):
    """The class for testing 'Hello World' app with the personal greeting and
    the showing of current weekday."""

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    def test_can_get_correct_username(self) -> None:
        """The function checks if user can get correct response with username."""
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue(username in response_text)

    def test_cannot_pass_incorrect_username(self) -> None:
        """The function checks if we get response with warning
        about incorrect username (for example username is two words)"""
        username = 'Хорошей среды'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue('Введено некорректное имя' in response_text)

    @freeze_time('2023-05-08')
    def test_can_get_correct_monday_response(self) -> None:
        """The function checks if user can get
        correct response if current weekday is monday."""
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue('понедельник' in response_text.lower())

    @freeze_time('2023-05-09')
    def test_can_get_correct_tuesday_response(self) -> None:
        """The function checks if user can get
        correct response if current weekday is tuesday."""
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue('вторник' in response_text.lower())

    @freeze_time('2023-05-10')
    def test_can_get_correct_wednesday_response(self) -> None:
        """The function checks if user can get
        correct response if current weekday is wednesday."""
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue('сред' in response_text.lower())

    @freeze_time('2023-05-11')
    def test_can_get_correct_thursday_response(self) -> None:
        """The function checks if user can get
        correct response if current weekday is thursday."""
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue('четверг' in response_text.lower())

    @freeze_time('2023-05-12')
    def test_can_get_correct_friday_response(self) -> None:
        """The function checks if user can get
        correct response if current weekday is friday."""
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue('пятниц' in response_text.lower())

    @freeze_time('2023-05-13')
    def test_can_get_correct_saturday_response(self) -> None:
        """The function checks if user can get
        correct response if current weekday is saturday."""
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue('суббот' in response_text.lower())

    @freeze_time('2023-05-14')
    def test_can_get_correct_sunday_response(self) -> None:
        """The function checks if user can get
        correct response if current weekday is sunday."""
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue('воскресень' in response_text.lower())


if __name__ == '__main__':
    unittest.main()
