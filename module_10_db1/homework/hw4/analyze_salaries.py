import sqlite3


def analyze_salaries(db_path: str) -> tuple:
    """
    The function analyzes database with people's salaries
    and returns tuple with results.
    :param db_path: the path to the source database
    """

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # 1. Get the quantity of poor people (less than 5000 guilders):
        cursor.execute(
            "SELECT COUNT(*) FROM salaries WHERE salary < 5000"
        )
        count_of_poor_people = cursor.fetchone()[0]

        # 2. Get the average salary:
        cursor.execute(
            "SELECT ROUND(AVG(salary), 2) FROM salaries"
        )
        average_salary = cursor.fetchone()[0]

        # 3. Get the median salary:
        cursor.execute(
            """
            SELECT ROUND(salary, 2) FROM salaries
            ORDER BY salary
            LIMIT 1 OFFSET (SELECT COUNT(*) FROM salaries) / 2
            """
        )
        median_salary = cursor.fetchone()[0]

        # 4. Get the number of social inequalities:
        cursor.execute(
            """
            SELECT SUM(salary)
            FROM (
                SELECT salary
                FROM salaries
                ORDER BY salary DESC
                LIMIT (SELECT COUNT(*) * 0.1 FROM salaries)
            )
            """
        )
        top_ten_percent_salary = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT SUM(salary)
            FROM (
                SELECT salary
                FROM salaries
                ORDER BY salary ASC
                LIMIT (SELECT COUNT(*) * 0.9 FROM salaries)
            )
            """
        )
        rest_ninety_percent_salary = cursor.fetchone()[0]

        number_of_inequalities = round(
            top_ten_percent_salary / rest_ninety_percent_salary * 100, 2
        )

        return (
            count_of_poor_people,
            average_salary,
            median_salary,
            number_of_inequalities
        )


if __name__ == "__main__":
    statistic = analyze_salaries("hw_4_database.db")
    print(
        f"""
        =====ИССЛЕДОВАНИЕ ДОХОДОВ НАСЕЛЕНИЯ=====\n
        1. За чертой бедности (зарплата меньше 5000 гульденов)
        находится {statistic[0]} человек(а).
        2. Средняя зарплата на острове: {statistic[1]} гульден(ов).
        3. Медианная зарплата на острове: {statistic[2]} гульден(ов).
        4. Число социального неравенства: {statistic[3]}%.
        """
    )
