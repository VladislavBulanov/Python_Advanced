import sqlite3


GET_SALARY_SQL = """
    SELECT salary
        FROM `table_effective_manager`
        WHERE name = ?;
"""

DELETE_EMPLOYEE_SQL = """
    DELETE FROM `table_effective_manager`
        WHERE name = ? AND name != "Иван Совин";
"""

UPDATE_SALARY_SQL = """
    UPDATE `table_effective_manager`
    SET salary = ?
    WHERE name = ? AND name != "Иван Совин";
"""


def ivan_sovin_the_most_effective(
        src_cursor: sqlite3.Cursor,
        src_name: str,
) -> None:
    """
    The function automizes the process of making decision
    about salary increasing of the specified employee.
    If potential salary will be more than manager's salary,
    the request is denied and employee is fired.
    Otherwise, the salary of employee is raised.
    :param src_cursor: the source sqlite3.Cursor
    :param src_name: the name of employee
    """

    employee_current_salary: int = src_cursor.execute(
        GET_SALARY_SQL, (src_name, )
    ).fetchone()[0]

    potential_employee_salary = employee_current_salary * 1.1

    if potential_employee_salary > IVAN_SOVIN_SALARY:
        src_cursor.execute(DELETE_EMPLOYEE_SQL, (src_name, ))
        return

    cursor.execute(UPDATE_SALARY_SQL, (potential_employee_salary, src_name))


if __name__ == '__main__':
    name: str = input('Введите имя сотрудника: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        IVAN_SOVIN_SALARY: int = cursor.execute(
            GET_SALARY_SQL, ("Иван Совин", )
        ).fetchone()[0]

        ivan_sovin_the_most_effective(cursor, name)
        conn.commit()
