import unittest

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
        """The function check if user can get correct response with username."""
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue(username in response_text)

    def test_can_get_correct_weekday(self) -> None:
        """The function check if user can get
        correct response with current weekday."""
