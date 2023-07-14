import sqlite3


SQL_QUERY: str = """
    SELECT *
        FROM `table_truck_with_vaccine`
        WHERE truck_number = ?
        AND temperature_in_celsius NOT BETWEEN ? AND ?
"""


def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str,
) -> bool:
    """
    The function checks if vaccine in the specified truck has spoiled.
    :param cursor: the source sqlite3.Cursor
    :param truck_number: the number of the source truck
    """

    cursor.execute(SQL_QUERY, (truck_number, 16, 20))
    not_in_right_temperature = cursor.fetchall()

    if len(not_in_right_temperature) < 3:
        return False
    return True


def main() -> None:
    """The main function of the app."""

    truck_number: str = input('Введите номер грузовика: ')

    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
        print('Испортилась' if spoiled else 'Не испортилась')


if __name__ == '__main__':
    main()
