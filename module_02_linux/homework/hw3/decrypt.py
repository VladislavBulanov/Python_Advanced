import sys


def decrypt(encryption: str) -> str:
    """
    The function decrypts the source encrypted message.
    :param encryption: the source encrypted message to decrypt
    """
    result = []
    for symbol in encryption:
        result.append(symbol)

        if len(result) >= 2 and result[-1] == '.' and result[-2] == '.':
            result.pop()
            result.pop()
            if result:
                result.pop()

    return ''.join(symbol for symbol in result if symbol != '.')


if __name__ == '__main__':
    data: str = sys.stdin.read()
    decryption: str = decrypt(data)
    print(decryption)
