import sqlite3


SQL_QUERY: str = """
    SELECT customer.full_name,
           manager.full_name,
           ord.purchase_amount,
           ord.date
    FROM `order` ord
    LEFT OUTER JOIN `customer` customer ON ord.customer_id = customer.customer_id
    LEFT OUTER JOIN `manager` manager ON ord.manager_id = manager.manager_id;
"""


if __name__ == "__main__":
    with sqlite3.connect("../hw.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        result = cursor.execute(SQL_QUERY).fetchall()
        print(len(result))
        for row in result:
            print(
                "Customer: {}, manager: {}, purchase amount: {}, date: {}".format(
                    row[0], row[1], row[2], row[3],
                )
            )
        conn.commit()
