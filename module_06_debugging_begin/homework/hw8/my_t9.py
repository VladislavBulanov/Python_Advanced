import os
import re
from typing import List, Tuple


with open(os.path.abspath('/usr/share/dict/words'), 'r') as file:
    ENGLISH_WORDS: Tuple[str] = tuple(word.strip() for word in file)


def my_t9(input_numbers: str) -> List[str]:
    """
    The function returns list of words which can be
    resulted by phone digital keyboard input.
    :param input_numbers: source digital string
    """

    decryption_dictionary = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz",
    }

    pattern = ""
    for number in input_numbers:
        pattern += f"[{decryption_dictionary[number]}]"

    matches: List[str] = []
    for word in ENGLISH_WORDS:
        result = re.fullmatch(pattern, word)
        if result:
            matches.append(result.group())

    return matches


if __name__ == '__main__':
    numbers: str = input("Input digital string (from 2 to 9): ")
    if all(re.match(r"[2-9]", symbol) for symbol in numbers):
        words: List[str] = my_t9(numbers)
        print(*words, sep='\n')
    else:
        print("String must consist of digits only from 2 to 9.")
