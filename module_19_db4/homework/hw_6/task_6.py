import sqlite3


if __name__ == "__main__":
    with sqlite3.connect("../../homework.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT ROUND(AVG(ag.grade),2) AS average_grade
            FROM assignments_grades ag
            WHERE ag.assignment_id IN (
                SELECT a.assignment_id
                FROM assignments a
                WHERE a.assignment_text LIKE "прочитать%"
                    OR a.assignment_text LIKE "выучить%"
            );
            """
        )
        result = cursor.fetchone()[0]
        print(
            "Средняя оценка заданий, где ученикам нужно что-то "
            "прочитать или выучить, равна", result
        )
