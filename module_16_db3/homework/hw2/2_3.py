import sqlite3

SQL_QUERY: str = """
    SELECT ord.order_no,
           manager.full_name,
           customer.full_name
    FROM `order` ord
    
    INNER JOIN `customer` customer
    ON ord.customer_id = customer.customer_id
    
    INNER JOIN `manager` manager
    ON ord.manager_id = manager.manager_id
    
    WHERE customer.city <> manager.city;
"""


if __name__ == "__main__":
    with sqlite3.connect("../hw.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        result = cursor.execute(SQL_QUERY).fetchall()
        for row in result:
            print(
                "Order number: {}, manager: {}, customer: {}".format(
                    row[0], row[1], row[2],
                )
            )
        conn.commit()
