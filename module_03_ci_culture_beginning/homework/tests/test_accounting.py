import unittest

from copy import deepcopy

from module_02_linux.homework.hw7.accounting import app, storage


class TestAccountingApp(unittest.TestCase):
    """The class for testing Flask app 'Accounting':
    the accounting of personal money spending."""

    TEST_DATA: dict = {
            '2023': {
                '1': {
                    '1': 500,
                    '10': 100,
                    'total': 600
                },
                '2': {
                    '18': 1000,
                    'total': 1000
                },
                '11': {
                    '5': 5000,
                    'total': 5000
                },
                'total': 6600
            }
        }

    @classmethod
    def setUpClass(cls) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        cls.app = app.test_client()
        storage.update(deepcopy(cls.TEST_DATA))

    @classmethod
    def tearDownClass(cls) -> None:
        storage.clear()

    def test_can_add_valid_expenses_in_valid_date(self) -> None:
        """The function checks if we can get correct response
        with valid date and valid expenses."""
        response = self.app.get('/add/20230107/100').data.decode()
        self.assertTrue('Запись успешно сохранена в базе данных!', response)
        storage.clear()
        storage.update(deepcopy(self.TEST_DATA))

    def test_cannot_add_invalid_expenses_in_valid_date(self) -> None:
        """The function checks if app returns response code 400
        if value of expenses is invalid (for example string)"""
        response = self.app.get('/add/20230501/abc')
        self.assertTrue(response.status_code == 404)

    def test_cannot_add_valid_expenses_in_invalid_date(self) -> None:
        """The function checks if we get response with message
        about incorrect date if date is invalid."""
        response = self.app.get('/add/2020501').data.decode()
        self.assertTrue(
            'Введённая дата не соответствует формату "YYYYMMDD".', response
        )

    def test_can_get_expenses_for_valid_existing_year(self) -> None:
        """The function checks if we get value of expenses
        for valid year existing in database."""
        response = self.app.get('/calculate/2023').data.decode()
        self.assertTrue('6600' in response)

    def test_can_get_expenses_for_valid_not_existing_year(self) -> None:
        """The function checks if we get value of expenses
        for valid year non-existing in database."""
        response = self.app.get('/calculate/2020').data.decode()
        self.assertTrue('составляют <b>0</b> руб.' in response)

    def test_cannot_get_expenses_for_invalid_years_format(self) -> None:
        """The function checks if we get warning
        message about invalid year's format."""
        response = self.app.get('/calculate/202').data.decode()
        self.assertEqual(
            'Введённый год не соответствует формату "YYYY".', response
        )

    def test_cannot_get_expenses_for_invalid_years_type(self) -> None:
        """The function checks if app returns '400'
        response code if year's type is string."""
        response = self.app.get('/calculate/abc')
        self.assertTrue(response.status_code == 404)

    def test_can_get_expenses_for_valid_date(self) -> None:
        """The function checks if we can get correct response
        with value of expenses in valid year and month."""
        response = self.app.get('/calculate/2023/01').data.decode()
        self.assertTrue('600' in response)

    def test_cannot_get_expenses_for_invalid_month_value(self) -> None:
        """The function checks if app returns warning
        message about incorrect month value."""
        response = self.app.get('/calculate/2023/15').data.decode()
        self.assertEqual('Некорректное значение года и/или месяца.', response)

    def test_cannot_get_expenses_for_invalid_month_type(self) -> None:
        """The function checks if response code
        is 400 if month's type is string."""
        response = self.app.get('/calculate/2023/abc')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
