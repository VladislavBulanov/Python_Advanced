import sys
from re import sub


def decrypt(encryption: str) -> str:
    """
    The function decrypts the source encrypted message.
    :param encryption: the source encrypted message to decrypt
    """
    result = sub(r'\.\.', '', encryption)
    result = sub(r'\.', lambda char: char.group(0)[:-1], result)
    return result


if __name__ == '__main__':
    data: str = sys.stdin.read()
    decryption: str = decrypt(data)
    print(decryption)
