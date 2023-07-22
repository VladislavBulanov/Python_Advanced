import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()

        # # For testing:
        # cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS `table_users` (
        #         id INTEGER PRIMARY KEY,
        #         username VARCHAR,
        #         password VARCHAR
        #     );
        # """)

        cursor.executescript(
            f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}')  
            """
        )
        conn.commit()


def hack() -> None:
    username: str = "', ''); DROP TABLE `table_users`; --"
    password: str = ""
    register(username, password)


if __name__ == '__main__':
    register('wignorbo', 'sjkadnkjasdnui31jkdwq')
    hack()
