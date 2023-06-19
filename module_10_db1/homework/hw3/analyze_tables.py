import sqlite3
from typing import List


def analyze_database(src_tables: List[str]) -> None:
    """
    The function prints results of
    specified tasks of database analysis.
    :param src_tables: the tables of source database
    """

    with sqlite3.connect("hw_3_database.db") as conn:
        cursor = conn.cursor()

        # 1. Get the count of rows in each table:
        print("1. Сколько записей хранится в каждой таблице:")
        for table in src_tables:
            cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
            count = cursor.fetchall()[0][0]
            print(f"- в таблице {table} {count} записи(ей)")

        # 2. Get unique rows in table_1:
        print("\n2. Сколько в таблице table_1 уникальных записей:")
        cursor.execute("SELECT DISTINCT * FROM `table_1`")
        print(len(cursor.fetchall()))

        # 3. Get the count of intersections of table_1 and table_2:
        print("\n3. Как много записей из таблицы "
              "table_1 встречается в table_2:")
        cursor.execute("SELECT * FROM `table_1` "
                       "INTERSECT SELECT * FROM `table_2`")
        print(len(cursor.fetchall()))

        # 4. Get the count of intersections of table_1, table_2 and table_3:
        print("\n4. Как много записей из таблицы table_1 "
              "встречается и в table_2, и в table_3:")
        cursor.execute("SELECT * FROM `table_1` "
                       "INTERSECT SELECT * FROM `table_2` "
                       "INTERSECT SELECT * FROM `table_3`")
        print(len(cursor.fetchall()))


if __name__ == "__main__":
    tables: List[str] = ["table_1", "table_2", "table_3"]
    analyze_database(tables)
