import sqlite3


if __name__ == "__main__":
    with sqlite3.connect("../../homework.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                sg.group_id AS group_id,
                COUNT(
                    CASE WHEN ag.date > a.due_date THEN 1 ELSE NULL END
                ) AS overdue_count
            FROM students_groups sg 
            LEFT JOIN assignments a
                ON sg.group_id = a.group_id
            LEFT JOIN assignments_grades ag
                ON a.assignment_id = ag.assignment_id
            GROUP BY sg.group_id;
            """
        )
        result = cursor.fetchall()
        print("Отчёт о просроченных заданиях:")
        print("Группа\tКол-во просроченных заданий")
        for row in result:
            print(f"{row[0]}\t\t{row[1]}")
