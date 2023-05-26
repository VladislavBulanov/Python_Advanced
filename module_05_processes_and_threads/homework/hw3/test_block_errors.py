import unittest
from block_errors import BlockErrors


class BlockErrorsTest(unittest.TestCase):
    """The class for testing context manager
    for blocking specified errors."""

    @staticmethod
    def test_ignore_specified_errors():
        """The function checks if context manager ignores specified errors."""

        error_types = {ZeroDivisionError}
        with BlockErrors(error_types):
            print(1 / 0)

    def test_do_not_ignore_not_specified_errors(self):
        """The function checks if context manager
        doesn't ignore not specified errors."""

        with self.assertRaises(TypeError):
            error_types = {ZeroDivisionError}
            with BlockErrors(error_types):
                print(1 / '0')

    @staticmethod
    def test_error_do_not_ignore_in_inner_block_and_ignore_in_outer_block():
        """The function checks if the error is thrown higher
        in the inner block and ignored in the outer block."""

        outer_error_types = {TypeError}
        with BlockErrors(outer_error_types):
            inner_error_types = {ZeroDivisionError}
            with BlockErrors(inner_error_types):
                print(1 / '0')


    @staticmethod
    def test_ignore_child_errors():
        """The function checks if context manager
        ignores child errors of specified parents."""

        error_types = {Exception}
        with BlockErrors(error_types):
            print(1 / '0')

    @staticmethod
    def test_no_error():
        """The function checks if context manager
        works correct without raised errors."""

        error_types = {ZeroDivisionError}
        with BlockErrors(error_types):
            print("")


if __name__ == '__main__':
    unittest.main()
