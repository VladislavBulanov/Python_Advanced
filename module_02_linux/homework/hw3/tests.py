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
    test_cases = (
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
    )

    for index, (data, expected) in enumerate(test_cases, start=1):
        result = decrypt(data)
        if result == expected:
            print(f'Test case {index}: Passed')
        else:
            print(f'Test case {index}: Failed')
            print(f'Expected: {expected}')
            print(f'Actual: {result}')
