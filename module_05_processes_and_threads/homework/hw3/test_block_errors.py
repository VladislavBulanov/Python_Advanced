import unittest
from block_errors import BlockErrors


class BlockErrorsTest(unittest.TestCase):
    def test_ignore_error(self):
        err_types = {ZeroDivisionError, TypeError}
        with BlockErrors(err_types):
            with self.assertRaises(Exception):
                a = 1 / 0

    def test_propagate_error(self):
        err_types = {ZeroDivisionError}
        with BlockErrors(err_types):
            with self.assertRaises(TypeError):
                a = 1 / '0'

    def test_inner_block_ignore_outer_error(self):
        outer_err_types = {TypeError}
        with BlockErrors(outer_err_types):
            inner_err_types = {ZeroDivisionError}
            with BlockErrors(inner_err_types):
                with self.assertRaises(TypeError):
                    a = 1 / '0'
        print("Внутренний блок: выполнено без ошибок")
        print("Внешний блок: выполнено без ошибок")

    def test_ignore_child_errors(self):
        err_types = {Exception}
        with BlockErrors(err_types):
            with self.assertRaises(Exception):
                a = 1 / '0'

    def test_no_error(self):
        err_types = set()
        with BlockErrors(err_types):
            a = 1 / 1


if __name__ == '__main__':
    unittest.main()
