import unittest
from flask_testing import TestCase
from remote_execution import app


class TestRemoteExecutionApp(TestCase):
    """The class for testing 'Remote Execution' app."""

    def create_app(self):
        """
        Create and configure the Flask app.
        :return: the configured Flask app.
        """

        app.config['TESTING'] = True
        app.config["WTF_CSRF_ENABLED"] = False
        return app

    def test_can_get_result_of_program_with_valid_data(self):
        """The function checks if user can get
        correct result of program with valid data."""

        with self.app.test_client() as client:
            response = client.post('/run_code', data={
                'code': 'print("Hello, World!")',
                'timeout': 5,
            })
            self.assert200(response)
            self.assertEqual(response.data.decode(), "Hello, World!\n")

    def test_cannot_run_program_without_code(self):
        """The function checks if user cannot run
        program with empty 'code' field."""

        with self.app.test_client() as client:
            response = client.post('/run_code', data={
                'timeout': 5,
            })
            self.assert400(response)
            self.assertIn(
                "The field 'code' is required", response.data.decode()
            )

    def test_cannot_run_program_with_invalid_python_code(self):
        """The function checks if user cannot run program
        with invalid Python code in the 'code' field."""

        with self.app.test_client() as client:
            response = client.post('/run_code', data={
                'code': 'print("Hello, World!"',
                'timeout': 5,
            })
            self.assert200(response)
            self.assertEqual("", response.data.decode())

    def test_cannot_run_program_with_non_digital_timeout(self):
        """The function checks if user cannot run program
        if value of 'timeout' field is not a number."""

        with self.app.test_client() as client:
            response = client.post('/run_code', data={
                'code': 'print("Hello, World!")',
                'timeout': 'abc',
            })
            self.assert400(response)
            self.assertIn(
                "Not a valid integer value", response.data.decode()
            )

    def test_cannot_run_program_with_timeout_out_of_range(self):
        """The function checks if user cannot run program
        if value of 'timeout' is not in range specified in validator."""

        with self.app.test_client() as client:
            response = client.post('/run_code', data={
                'code': 'print("Hello, World!")',
                'timeout': 60,
            })
            self.assert400(response)
            self.assertIn(
                "Number must be between 1 and 30", response.data.decode()
            )

    def test_cannot_run_program_without_timeout(self):
        """The function checks if user cannot run
        program with empty 'timeout' field."""

        with self.app.test_client() as client:
            response = client.post('/run_code', data={
                'code': 'print("Hello, World!")',
            })
            self.assert400(response)
            self.assertIn(
                "The field 'timeout' is required", response.data.decode()
            )

    def test_cannot_get_result_if_timeout_is_less_than_performing(self):
        """The function checks if user cannot get of result of program
        if timeout is less than time of program's execution."""

        with self.app.test_client() as client:
            response = client.post('/run_code', data={
                'code': '999**1000000000000000000',
                'timeout': 1,
            })
            self.assert200(response)
            self.assertEqual(
                "Execution time exceeded the timeout limit.", response.data.decode()
            )

    def test_cannot_run_program_with_shell_commands(self):
        """The function checks if user cannot run program
        with shell commands in the 'code' field."""

        with self.app.test_client() as client:
            response = client.post('/run_code', data={
                'code': 'print("Hello, World!"); echo "hacked"',
                'timeout': 5,
            })
            self.assert200(response)
            self.assertEqual(
                "", response.data.decode()
            )


if __name__ == '__main__':
    unittest.main()
