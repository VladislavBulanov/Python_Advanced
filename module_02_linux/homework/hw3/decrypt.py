import sys


def decrypt(encryption: str) -> str:
    """
    The function decrypts the source encrypted message.
    :param encryption: the source encrypted message to decrypt
    """
    result = ''
    symbol_index = 0
    while symbol_index < len(encryption):
        if encryption[symbol_index] == '.':
            if symbol_index + 1 < len(encryption) and \
                    encryption[symbol_index + 1] == '.':
                if result:
                    result = result[:-1]
                symbol_index += 1

        else:
            result += encryption[symbol_index]

        symbol_index += 1
    return result


if __name__ == '__main__':
    data: str = sys.stdin.read()
    decryption: str = decrypt(data)
    print(decryption)
