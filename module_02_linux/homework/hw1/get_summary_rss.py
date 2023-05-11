import os
from typing import List


def get_summary_rss(ps_output_file_path: str) -> str:
    """
    The function takes the path to the file with data of current system's
    processes and returns total amount of memory consumed.
    :param ps_output_file_path: path to source file
    """
    try:
        with open(ps_output_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()[1:]
            columns: List[List[str]] = [line.split() for line in lines]
            total_memory_b = sum((int(record[5]) for record in columns))
            total_memory_kb = round(total_memory_b / 1e+3, 2)
            total_memory_mb = round(total_memory_b / 1e+6, 2)
            total_memory_gb = round(total_memory_b / 1e+9, 2)
            return ('Суммарный объём потребляемой памяти равен '
                    '{} Б или {} КБ или {} МБ или {} ГБ'.format(
                        total_memory_b,
                        total_memory_kb,
                        total_memory_mb,
                        total_memory_gb,
                    ))
    except FileNotFoundError:
        return 'Файл по указанному пути не найден.'


if __name__ == '__main__':
    path: str = os.path.abspath('output_file.txt')
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)
