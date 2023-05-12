import unittest

from module_02_linux.homework.hw3.decrypt import decrypt


class TestDecryption(unittest.TestCase):

    def test_1(self):
        data = 'абра-кадабра.'
        expected_result = 'абра-кадабра'
        function_result = decrypt(data)
        self.assertEqual(expected_result, function_result)

    def test_2(self):
        data = 'абраа..-кадабра'
        expected_result = 'абра-кадабра'
        function_result = decrypt(data)
        self.assertEqual(expected_result, function_result)

    def test_3(self):
        data = 'абраа..-.кадабра'
        expected_result = 'абра-кадабра'
        function_result = decrypt(data)
        self.assertEqual(expected_result, function_result)

    def test_4(self):
        data = 'абра--..кадабра'
        expected_result = 'абра-кадабра'
        function_result = decrypt(data)
        self.assertEqual(expected_result, function_result)

    def test_5(self):
        data = 'абрау...-кадабра'
        expected_result = 'абра-кадабра'
        function_result = decrypt(data)
        self.assertEqual(expected_result, function_result)

    def test_6(self):
        data = 'абра........'
        expected_result = ''
        function_result = decrypt(data)
        self.assertEqual(expected_result, function_result)

    def test_7(self):
        data = 'абр......a.'
        expected_result = 'a'
        function_result = decrypt(data)
        self.assertEqual(expected_result, function_result)

    def test_8(self):
        data = '1..2.3'
        expected_result = '23'
        function_result = decrypt(data)
        self.assertEqual(expected_result, function_result)

    def test_9(self):
        data = '.'
        expected_result = ''
        function_result = decrypt(data)
        self.assertEqual(expected_result, function_result)

    def test_10(self):
        data = '1.......................'
        expected_result = ''
        function_result = decrypt(data)
        # self.assertEqual(expected_result, function_result)
        self.assertTrue(expected_result == function_result)
