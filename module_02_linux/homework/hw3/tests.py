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
    test_cases = [
        ('абра-кадабра.', 'абра-кадабра'),
        ('абраа..-кадабра', 'абра-кадабра'),
        ('абраа..-.кадабра', 'абра-кадабра'),
        ('абра--..кадабра', 'абра-кадабра'),
        ('абрау...-кадабра', 'абра-кадабра'),
        ('абра........', ''),
        ('абр......a.', 'a'),
        ('1..2.3', '23'),
        ('.', ''),
        ('1.......................', '')
    ]

    for index, (data, expected) in enumerate(test_cases, start=1):
        decrypted = decrypt(data)
        if decrypted == expected:
            print(f'Test case {index}: Passed')
        else:
            print(f'Test case {index}: Failed')
            print(f'Expected: {expected}')
            print(f'Actual: {decrypted}')
