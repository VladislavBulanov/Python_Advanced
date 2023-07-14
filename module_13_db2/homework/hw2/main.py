import csv
import sqlite3


SQL_QUERY_TO_DELETE = """
    DELETE FROM `table_fees`
        WHERE truck_number = ? AND timestamp = ?
"""


def delete_wrong_fees(
        cursor: sqlite3.Cursor,
        wrong_fees_file: str,
) -> None:
    """
    The function deletes the wrong fees in the source database.
    The wrong fees are specified in CSV-file.
    :param cursor: the source sqlite3.Cursor
    :param wrong_fees_file: the CSV-file with wrong fees
    """

    with open(wrong_fees_file) as csvfile:
        fees_data = csv.reader(csvfile)

        for record in fees_data:
            car_number, timestamp = record
            cursor.execute(SQL_QUERY_TO_DELETE, (car_number, timestamp))


def main() -> None:
    """The main function of the app."""

    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        delete_wrong_fees(cursor, "../wrong_fees.csv")
        conn.commit()


if __name__ == "__main__":
    main()
