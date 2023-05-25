import sys
import unittest
from io import StringIO
from redirect import Redirect


class RedirectTestCase(unittest.TestCase):
    """The class for testing threads' redirect program."""

    def test_redirect_stdout_only(self):
        """The function redirects stdout only, stderr remains unchanged."""

        original_stderr = sys.stderr
        output = StringIO()
        with Redirect(stdout=output):
            print('Hello stdout')
            raise Exception('Hello stderr')
        self.assertEqual(output.getvalue().strip(), 'Hello stdout')
        self.assertEqual(sys.stderr, original_stderr)

    def test_redirect_stderr_only(self):
        """The function redirects stderr only, stdout remains unchanged."""

        original_stdout = sys.stdout
        output = StringIO()
        with Redirect(stderr=output):
            print('Hello stdout')
            raise Exception('Hello stderr')
        self.assertEqual(sys.stdout, original_stdout)
        self.assertIn('Exception: Hello stderr', output.getvalue().strip())

    def test_both_redirected(self):
        """The function redirects both stdout and stderr."""

        stdout_output = StringIO()
        stderr_output = StringIO()
        with Redirect(stdout=stdout_output, stderr=stderr_output):
            print('Hello stdout')
            raise Exception('Hello stderr')
        self.assertEqual(stdout_output.getvalue().strip(), 'Hello stdout')
        self.assertIn(
            'Exception: Hello stderr', stderr_output.getvalue().strip()
        )

    def test_no_redirect(self):
        """The function redirects neither stdout and stderr."""

        original_stdout = sys.stdout
        original_stderr = sys.stderr

        with Redirect():
            print('Hello stdout')
            raise Exception('Hello stderr')

        self.assertIs(sys.stdout, original_stdout)
        self.assertIs(sys.stderr, original_stderr)


if __name__ == '__main__':
    with open('test_results.txt', 'a') as test_file_stream:
        runner = unittest.TextTestRunner(stream=test_file_stream)
        unittest.main(testRunner=runner)
