import sqlite3


def find_amount_of_students_in_each_group(cur: sqlite3.Cursor) -> None:
    """A function prints the amount of students in each group."""

    cur.execute(
        """
        SELECT
            s.group_id AS group_id,
            COUNT(*) AS students_amount
        FROM students s
        LEFT JOIN students_groups sg
            ON s.group_id = sg.group_id
        GROUP BY s.group_id;
        """
    )
    result = cur.fetchall()
    print("\n===== КОЛИЧЕСТВО СТУДЕНТОВ В КАЖДОЙ ГРУППЕ =====")
    print("\t\t№\t\tКол-во студентов")
    for row in result:
        print(f"\t\t{row[0]}\t\t{row[1]}")


def find_average_grade_in_each_group(cur: sqlite3.Cursor) -> None:
    """A function prints the average grade of students in each group."""

    cur.execute(
        """
        SELECT
            s.group_id AS group_id,
            ROUND(AVG(ag.grade), 2) AS average_grade 
        FROM students s
        LEFT JOIN assignments_grades ag
            ON s.student_id = ag.student_id
        GROUP BY s.group_id;
        """
    )
    result = cur.fetchall()
    print("\n===== СРЕДНИЙ БАЛЛ В КАЖДОЙ ГРУППЕ =====")
    print("\t\t№\t\tСр. балл")
    for row in result:
        print(f"\t\t{row[0]}\t\t{row[1]}")


def find_amount_of_students_not_submitted_work_in_each_group(
        cur: sqlite3.Cursor,
) -> None:
    """A function prints the amount of students
    in each group who did not submit the work."""

    cur.execute(
        """
        SELECT
            s.group_id AS group_id,
            COUNT(*) AS not_submitted_amount
        FROM students s
        LEFT JOIN assignments_grades ag
            ON s.student_id = ag.student_id
        WHERE ag.grade IS NULL
        GROUP BY s.group_id;
        """
    )
    result = cur.fetchall()
    print("\n===== КОЛ-ВО СТУДЕНТОВ, НЕСДАВШИХ РАБОТУ =====")
    print("\t\t№\t\tКол-во")
    for row in result:
        print(f"\t\t{row[0]}\t\t{row[1]}")


def find_amount_of_overdue_in_each_group(cur: sqlite3.Cursor) -> None:
    """A function prints the amount of students in each group who
    have missed the deadline for the completion of the work."""

    cur.execute(
        """
        SELECT
            s.group_id AS group_id,
            COUNT(*) AS overdue_amount
        FROM students s
        LEFT JOIN assignments_grades ag
            ON s.student_id = ag.student_id
        LEFT JOIN assignments a
            ON ag.assignment_id = a.assignment_id
        WHERE ag.date > a.due_date
        GROUP BY s.group_id;
        """
    )
    result = cur.fetchall()
    print("\n===== КОЛ-ВО СТУДЕНТОВ, НЕСДАВШИХ РАБОТУ ВОВРЕМЯ =====")
    print("\t\t№\t\tКол-во")
    for row in result:
        print(f"\t\t{row[0]}\t\t{row[1]}")


def find_amount_of_repeated_attempts_in_each_group(cur: sqlite3.Cursor) -> None:
    """A function prints the amount of repeated attempts to submit the work."""

    cur.execute(
        """
        SELECT
            s.group_id AS group_id,
            COUNT(repeated_attempts.assignment_id) / 2 AS repeated_attempts
        FROM assignments_grades ag
        -- Join results with students to know students groups:
        JOIN students s
            ON ag.student_id  = s.student_id
        -- Join with subtable to find all cases of several attempts:
        LEFT JOIN (
            -- Find cases when student submitted the work several times:
            SELECT
                assignment_id,
                student_id
            FROM
                assignments_grades
            GROUP BY
                assignment_id,
                student_id
            HAVING
                COUNT(*) > 1
        ) AS repeated_attempts
        ON ag.assignment_id = repeated_attempts.assignment_id
            AND s.student_id = repeated_attempts.student_id
        GROUP BY s.group_id;
        """
    )
    result = cur.fetchall()
    print("\n===== КОЛ-ВО ПОВТОРНЫХ ПОПЫТОК СДАТЬ РАБОТУ =====")
    print("\t\t№\t\tКол-во")
    for row in result:
        print(f"\t\t{row[0]}\t\t{row[1]}")


if __name__ == "__main__":
    print("========== ОТЧЁТ О ГРУППАХ ==========")
    with sqlite3.connect("../../homework.db") as conn:
        cursor = conn.cursor()
        find_amount_of_students_in_each_group(cursor)
        find_average_grade_in_each_group(cursor)
        find_amount_of_students_not_submitted_work_in_each_group(cursor)
        find_amount_of_overdue_in_each_group(cursor)
        find_amount_of_repeated_attempts_in_each_group(cursor)
