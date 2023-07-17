import datetime
import sqlite3


INSERT_SQL_QUERY = """
    INSERT INTO `table_birds` (datetime, name, count)
        VALUES (?, ?, ?);
"""

GET_COUNT_OF_LOGS_OF_SOURCE_BIRD_SQL_QUERY = """
    SELECT COUNT(*)
        FROM `table_birds`
        WHERE name = ?;
"""


def log_bird(
        cursor: sqlite3.Cursor,
        bird_name: str,
        bird_quantity: int,
        date_time: str,
) -> None:
    """
    The function records the log about bird in the source database.
    :param cursor: the source sqlite3.Cursor
    :param bird_name: the name of the bird
    :param bird_quantity: the quantity of the bird was seen
    :param date_time: the datetime when the bird was seen
    """

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS table_birds (
            id integer PRIMARY KEY,
            datetime varchar,
            name varchar,
            count integer
        );
    """)

    cursor.execute(INSERT_SQL_QUERY, (date_time, bird_name, bird_quantity))


def check_if_such_bird_already_seen(
        cursor: sqlite3.Cursor,
        bird_name: str,
) -> bool:
    """
    The function checks if the specified bird has already been seen before.
    :param cursor: the source sqlite3.Cursor
    :param bird_name: the name of the bird
    """

    cursor.execute(GET_COUNT_OF_LOGS_OF_SOURCE_BIRD_SQL_QUERY, (bird_name, ))
    logs_quantity, *_ = cursor.fetchone()
    return logs_quantity > 1


def main() -> None:
    """The main function of the app."""

    print("Программа помощи ЮНатам v0.1")
    name: str = input("Пожалуйста, введите имя птицы\n> ")
    count_str: str = input("Сколько птиц вы увидели?\n> ")
    count: int = int(count_str)
    right_now: str = datetime.datetime.utcnow().isoformat()

    with sqlite3.connect("../homework.db") as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        log_bird(cursor, name, count, right_now)

        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")

        connection.commit()


if __name__ == "__main__":
    main()
