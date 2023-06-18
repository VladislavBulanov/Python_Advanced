import sqlite3
from typing import Tuple, Union


def analyze_salaries(db_path: str) -> Tuple[Union[int, float]]:
    """
    The function analyzes database with people's salaries
    and returns tuple with results.
    :param db_path: the path to the source database
    """

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # 1. Get the quantity of poor people (less than 5000 guilders):
        cursor.execute(
            "SELECT `salary` FROM `salaries` WHERE `salary` < 5000"
        )
        print(cursor.fetchall())


        # For testing:
        cursor.execute("SELECT `salary` FROM `salaries`")
        salaries: Tuple[int] = sorted(tuple(record[0] for record in cursor.fetchall()))
        # print(salaries)
        print(f"Total: {len(salaries)}")

        # 1:
        print(f"Low sal: {len(tuple(salary for salary in salaries if salary < 5000))}")

        # 2:
        print(f"Avg: {sum(salaries) / len(salaries)}")

        # 3:
        mid_index = len(salaries) // 2 - 1
        med_sal = (salaries[mid_index] + salaries[mid_index + 1]) / 2
        print(f"Med: {med_sal}")
        low = len([sal for sal in salaries if sal <= med_sal])
        high = len([sal for sal in salaries if sal >= med_sal])
        print(low, high)

        # 4:
        cursor.execute("SELECT COUNT(`salary`) FROM `salaries`")
        print(cursor.fetchall())


if __name__ == "__main__":
    statistic = analyze_salaries("hw_4_database.db")
