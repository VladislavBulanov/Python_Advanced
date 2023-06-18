from typing import Union, List

Number = Union[int, float, complex]


def find_insert_position(array: List[Number], number: Number) -> int:
    """
    The function returns an index showing
    where the specified number needs to be inserted
    in order for the array to remain sorted.
    The function uses binary search.
    :param array: source array
    :param number: inputted number
    """

    left = 0
    right = len(array)

    while left < right:
        mid = (left + right) // 2
        if array[mid] < number:
            left = mid + 1
        else:
            right = mid

    return left


if __name__ == '__main__':
    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    insert_position: int = find_insert_position(A, x)
    assert insert_position == 5

    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    A.insert(insert_position, x)
    assert A == sorted(A)

    A: List[Number] = []
    x: Number = 4
    insert_position: int = find_insert_position(A, x)
    assert insert_position == 0

    A: List[Number] = []
    x: Number = 4
    A.insert(insert_position, x)
    assert A == sorted(A)

    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = -1
    insert_position: int = find_insert_position(A, x)
    assert insert_position == 0

    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = -1
    A.insert(insert_position, x)
    assert A == sorted(A)

    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 10
    insert_position: int = find_insert_position(A, x)
    assert insert_position == 6

    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 10
    A.insert(insert_position, x)
    assert A == sorted(A)
