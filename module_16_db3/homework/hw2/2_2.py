import sqlite3


SQL_QUERY: str = """
    SELECT customer.full_name
    FROM `customer` customer
    LEFT OUTER JOIN `order` ord
    ON customer.customer_id = ord.customer_id
    WHERE ord.customer_id IS NULL;
"""


if __name__ == "__main__":
    with sqlite3.connect("../hw.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        result = cursor.execute(SQL_QUERY).fetchall()
        for row in result:
            print(*row)
        conn.commit()
