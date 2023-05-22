import unittest
from flask_testing import TestCase
from hw1_registration import app


class RegistrationFormTest(TestCase):
    """The class for testing Flask registration form."""

    def create_app(self):
        app.config['TESTING'] = True
        app.config["WTF_CSRF_ENABLED"] = False
        return app

    def test_can_register_with_valid_registration_data(self):
        """The function checks if user can
        register with valid registration data."""

        with self.app.test_client() as client:
            response = client.post('/registration', data={
                'email': 'vladi_18@google.com',
                'phone': '9998887766',
                'name': 'Vladislav Bulanov',
                'address': 'Moscow',
                'index': '101000',
                'comment': 'Sample comment.'
            })
            self.assert200(response)
            self.assertEqual(response.data.decode(),
                             "Successfully registered user vladi_18@google.com"
                             " with phone +79998887766")

    def test_cannot_register_with_invalid_email(self):
        """The function checks if user cannot register with invalid email."""

        with self.app.test_client() as client:
            response = client.post('/registration', data={
                'email': 'invalid_email',
                'phone': '9998887766',
                'name': 'Vladislav Bulanov',
                'address': 'Moscow',
                'index': '101000',
                'comment': 'Sample comment.'
            })
            self.assert400(response)
            self.assertIn(
                "The field 'email' is invalid format", response.data.decode()
            )

    def test_cannot_register_without_email(self):
        """The function checks if user cannot register without email."""

        with self.app.test_client() as client:
            response = client.post('/registration', data={
                'phone': '9998887766',
                'name': 'Vladislav Bulanov',
                'address': 'Moscow',
                'index': '101000',
                'comment': 'Sample comment.'
            })
            self.assert400(response)
            self.assertIn(
                "The field 'email' is required", response.data.decode()
            )

    def test_cannot_register_with_invalid_phone_length(self):
        """The function checks if user cannot
        register with invalid phone length."""

        with self.app.test_client() as client:
            response = client.post('/registration', data={
                'email': 'vladi_18@google.com',
                'phone': '999',
                'name': 'Vladislav Bulanov',
                'address': 'Moscow',
                'index': '101000',
                'comment': 'Sample comment.'
            })
            self.assert400(response)
            self.assertIn(
                "The phone number must consist of ten digits",
                response.data.decode()
            )

    def test_cannot_register_with_invalid_phone_type(self):
        """The function checks if user cannot
        register with invalid phone's type."""

        with self.app.test_client() as client:
            response = client.post('/registration', data={
                'email': 'vladi_18@google.com',
                'phone': 'abc',
                'name': 'Vladislav Bulanov',
                'address': 'Moscow',
                'index': '101000',
                'comment': 'Sample comment.'
            })
            self.assert400(response)
            self.assertIn("Not a valid integer value", response.data.decode())

    def test_cannot_register_without_phone(self):
        """The function checks if user cannot register without phone."""

        with self.app.test_client() as client:
            response = client.post('/registration', data={
                'email': 'vladi_18@google.com',
                'name': 'Vladislav Bulanov',
                'address': 'Moscow',
                'index': '101000',
                'comment': 'Sample comment.'
            })
            self.assert400(response)
            self.assertIn(
                "The field 'phone' is required", response.data.decode()
            )

    def test_cannot_register_without_name(self):
        """The function checks if user cannot register without name."""

        with self.app.test_client() as client:
            response = client.post('/registration', data={
                'email': 'vladi_18@google.com',
                'phone': '9998887766',
                'address': 'Moscow',
                'index': '101000',
                'comment': 'Sample comment.'
            })
            self.assert400(response)
            self.assertIn(
                "The field 'name' is required", response.data.decode()
            )

    def test_cannot_register_without_address(self):
        """The function checks if user cannot register without address."""

        with self.app.test_client() as client:
            response = client.post('/registration', data={
                'email': 'vladi_18@google.com',
                'phone': '9998887766',
                'name': 'Vladislav Bulanov',
                'index': '101000',
                'comment': 'Sample comment.'
            })
            self.assert400(response)
            self.assertIn(
                "The field 'address' is required", response.data.decode()
            )

    def test_cannot_register_with_invalid_index_type(self):
        """The function checks if user cannot
        register with invalid index type."""

        with self.app.test_client() as client:
            response = client.post('/registration', data={
                'email': 'vladi_18@google.com',
                'phone': '9998887766',
                'name': 'Vladislav Bulanov',
                'address': 'Moscow',
                'index': 'abc',
                'comment': 'Sample comment.'
            })
            self.assert400(response)
            self.assertIn("Not a valid integer value", response.data.decode())

    def test_cannot_register_without_index(self):
        """The function checks if user cannot register without index."""

        with self.app.test_client() as client:
            response = client.post('/registration', data={
                'email': 'vladi_18@google.com',
                'phone': '9998887766',
                'name': 'Vladislav Bulanov',
                'address': 'Moscow',
                'comment': 'Sample comment.'
            })
            self.assert400(response)
            self.assertIn(
                "The field 'index' is required", response.data.decode()
            )

    def test_can_register_without_comment(self):
        """The function checks if user can register
        without comment (this field is optional)."""

        with self.app.test_client() as client:
            response = client.post('/registration', data={
                'email': 'vladi_18@google.com',
                'phone': '9998887766',
                'name': 'Vladislav Bulanov',
                'address': 'Moscow',
                'index': '101000'
            })
            self.assert200(response)
            self.assertEqual(response.data.decode(),
                             "Successfully registered user vladi_18@google.com"
                             " with phone +79998887766")


if __name__ == '__main__':
    unittest.main()
