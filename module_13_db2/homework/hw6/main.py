import sqlite3
from copy import copy
from datetime import datetime, timedelta
from typing import List, Dict


TRAININGS_BY_DAYS: Dict[int, str] = {
    0: "футбол",
    1: "хоккей",
    2: "шахматы",
    3: "SUP-серфинг",
    4: "бокс",
    5: "Dota2",
    6: "шахбокс",
}


def update_work_schedule(src_cursor: sqlite3.Cursor) -> None:
    """
    The function updates the database with schedule
    based on employees' sport preferences.
    :param src_cursor: the source sqlite3.Cursor
    """

    # 1. Empty the source table with old schedule:
    src_cursor.execute(
        """
        DELETE FROM `table_friendship_schedule`
        """
    )

    # 2. Get the list of employees and his preferable sport:
    src_employees: List[tuple] = src_cursor.execute(
        """
        SELECT id, preferable_sport
        FROM `table_friendship_employees`;
        """
    ).fetchall()

    # 3. Make a copy of the list of employees for taking
    # him from this list and putting him in the schedule.
    # When length of the list become less than 7 employees
    # the list is extended by source employees' list.
    employees = copy(src_employees)

    # 4. Start filling a schedule from the first day of the year day-by-day:
    current_date = datetime(2020, 1, 1)
    # 366 days in case the year is a leap year:
    for day_of_the_year in range(366):
        current_weekday = current_date.weekday()

        # Make a list of employees for current day consisting of 10 employees:
        current_day_squad: List[tuple] = []
        for _ in range(10):

            for index, employee in enumerate(employees):
                # If in current day of the week current employee has
                # no training he is added in a current day squad.
                # Else he is skipped:
                if employee[1] != TRAININGS_BY_DAYS.get(current_weekday):
                    current_day_squad.append(
                        (employee[0], current_date.isoformat().split("T")[0])
                    )
                    employees.pop(index)

                    # Check the length of a list of available employees:
                    if len(employees) < 7:
                        employees.extend(copy(src_employees))

                    break

                else:
                    continue

        # Push a current day squad in a schedule:
        src_cursor.executemany(
            """
            INSERT INTO `table_friendship_schedule` (employee_id, date)
            VALUES (?, ?);
            """, current_day_squad
        )
        # Step to the next day:
        current_date += timedelta(days=1)


if __name__ == '__main__':
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        update_work_schedule(cursor)
        conn.commit()
