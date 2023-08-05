import sqlite3

SQL_SCRIPT: str = """

"""

if __name__ == "__main__":
    with sqlite3.connect("../hw.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.executescript(SQL_SCRIPT)
        conn.commit()
