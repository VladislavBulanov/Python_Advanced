import sys
from typing import List, Union


def get_mean_size(ls_output: List[str]) -> Union[float, str]:
    """
    The function receives data from output file and
    returns mean size of file in initial directory
    or error message if initial directory is empty
    or data cannot be retrieved.
    :param ls_output: data from output file
    """
    if ls_output:
        try:
            total_sum = sum(float(line.split()[4])for line in ls_output)
            return round(total_sum / len(ls_output), 2)
        except Exception:
            return 'Что-то пошло не так...'

    return 'В данной директории нет файлов.'


if __name__ == '__main__':
    data: List[str] = sys.stdin.readlines()[1:]
    mean_size: float = get_mean_size(data)
    print(mean_size)
