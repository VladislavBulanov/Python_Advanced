import sqlite3


SQL_QUERY: str = """
    SELECT customer.full_name,
           ord.order_no
    FROM `order` ord
    
    INNER JOIN `customer` customer
    ON ord.customer_id = customer.customer_id
    
    WHERE ord.manager_id IS NULL;
"""


if __name__ == "__main__":
    with sqlite3.connect("../hw.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        result = cursor.execute(SQL_QUERY).fetchall()
        for row in result:
            print(
                "Customer: {}, order number: {}".format(
                    row[0], row[1],
                )
            )
        conn.commit()
