import sqlite3


if __name__ == "__main__":
    with sqlite3.connect("../../homework.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                s.student_id AS student_id,
                s.full_name AS student_name
            FROM `students` s
            JOIN `students_groups` sg ON s.group_id = sg.group_id
            WHERE sg.teacher_id = (
                SELECT a.teacher_id
                FROM `assignments` a
                JOIN `assignments_grades` ag
                    ON a.assignment_id = ag.assignment_id
                GROUP BY a.teacher_id
                ORDER BY AVG(ag.grade) DESC
                LIMIT 1
            )
            """
        )
        result = cursor.fetchall()
        print("Ученики преподавателя с самыми простыми заданиями:")
        print("№\t\tID\t\tФИО\t\t")
        for index, row in enumerate(result, start=1):
            print(
                "{index})\t\t{id}\t\t{name}".format(
                    index=index,
                    id=row[0],
                    name=row[1],
                )
            )
