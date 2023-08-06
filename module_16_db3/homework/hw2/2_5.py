import sqlite3


SQL_QUERY: str = """
    SELECT DISTINCT customer1.full_name, customer2.full_name
    FROM `customer` customer1
    INNER JOIN `customer` customer2
    ON customer1.city = customer2.city
    AND customer1.manager_id = customer2.manager_id
    WHERE customer1.customer_id <> customer2.customer_id;
"""


if __name__ == "__main__":
    with sqlite3.connect("../hw.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        result = cursor.execute(SQL_QUERY).fetchall()
        for row in result:
            print(*row)
        conn.commit()
