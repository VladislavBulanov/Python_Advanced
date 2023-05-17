import unittest
from decrypt import decrypt


class TestDecryptionFunction(unittest.TestCase):
    """The class for testing function for decryption."""

    def test_even_amount_of_dots_encryption(self) -> None:
        """The function checks if we get correct decryption
        if encryption has even quantity of dots."""
        self.assertEqual(decrypt('абра-кадабра.'), 'абра-кадабра')
        self.assertEqual(decrypt('абраа..-.кадабра'), 'абра-кадабра')
        self.assertEqual(decrypt('абрау...-кадабра'), 'абра-кадабра')
        self.assertEqual(decrypt('абр......a.'), 'a')
        self.assertEqual(decrypt('1..2.3'), '23')
        self.assertEqual(decrypt('.'), '')
        self.assertEqual(decrypt('1.......................'), '')

    def test_odd_amount_of_dots_encryption(self) -> None:
        """The function checks if we get correct decryption
        if encryption has odd quantity of dots."""
        self.assertEqual(decrypt('абраа..-кадабра'), 'абра-кадабра')
        self.assertEqual(decrypt('абра--..кадабра'), 'абра-кадабра')
        self.assertEqual(decrypt('абра........'), '')


if __name__ == '__main__':
    unittest.main()
