import unittest

from module_02_linux.homework.hw5.max_number import app


class TestMaxNumberApp(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/max_number/'

    def test_can_get_correct_max_number_in_series_of_two(self):
        numbers = 1, 2
        url = self.base_url + '/'.join(str(num) for num in numbers)
        response = self.app.get(url)
        response_text = response.data.decode()
        correct_answer_str = f'{max(numbers)}'
        self.assertTrue(correct_answer_str in response_text)
