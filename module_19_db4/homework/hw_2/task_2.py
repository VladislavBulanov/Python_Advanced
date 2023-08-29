import sqlite3


if __name__ == "__main__":
    with sqlite3.connect("../../homework.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                s.student_id AS student_id,
                s.full_name AS student_name,
                AVG(ag.grade) AS average_grade
            FROM `students` s
            JOIN `assignments_grades` ag ON s.student_id = ag.student_id
            GROUP BY s.student_id
            ORDER BY average_grade DESC
            LIMIT 10
            """
        )
        result = cursor.fetchall()
        print("Десять лучших учеников:")
        for index, row in enumerate(result, start=1):
            print(
                "{})\t\tID: {}\t\tФИО: {}\t\tсредний балл: {}".format(
                    index,
                    row[0],
                    row[1],
                    row[2],
                )
            )
