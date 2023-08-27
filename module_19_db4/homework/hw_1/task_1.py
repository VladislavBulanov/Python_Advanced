import sqlite3


if __name__ == "__main__":
    with sqlite3.connect("../../homework.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                t.teacher_id AS teacher_id,
                t.full_name AS teacher_name,
                AVG(ag.grade) AS average_grade
            FROM `teachers` t
            JOIN `assignments` a ON t.teacher_id = a.teacher_id
            JOIN `assignments_grades` ag
                ON a.assignment_id = ag.assignment_id
            GROUP BY t.teacher_id
            ORDER BY average_grade ASC
            """
        )
        result = cursor.fetchone()
        print("Самые сложные задания задаёт следующий преподаватель:")
        print("ID: {}\nФИО: {}\nСредний балл: {}".format(
            result[0],
            result[1],
            result[2],
        ))
