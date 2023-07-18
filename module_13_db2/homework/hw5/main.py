import sqlite3
from random import sample
from typing import List, Tuple

from uefa_teams import TEAMS


def generate_test_data(
        cursor: sqlite3.Cursor,
        number_of_groups: int,
) -> None:
    """
    The function fills the database 'uefa_commands' with UEFA teams
    according number of groups and teams' levels. Then function fills
    the database 'uefa_draw' with results of the draw.
    :param cursor: the source sqlite3.Cursor
    :param number_of_groups: the amount of groups
    """

    # Create list of teams:
    teams: List[Tuple[str]] = []
    top_teams = sample(TEAMS["Top"], number_of_groups)
    normal_teams = sample(TEAMS["Normal"], number_of_groups * 2)
    weak_teams = sample(TEAMS["Weak"], number_of_groups)
    teams.extend(top_teams)
    teams.extend(normal_teams)
    teams.extend(weak_teams)

    # Fill 'uefa_commands' table:
    cursor.executemany("""
        INSERT INTO `uefa_commands`
            (command_name, command_country, command_level)
            VALUES (?, ?, ?);
    """, teams)

    # Make draw:


def main() -> None:
    """The main function of the app."""

    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))
    if number_of_groups not in range(4, 17):
        print("Вы ввели неверное количество групп.")
        return

    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        generate_test_data(cursor, number_of_groups)
        conn.commit()


if __name__ == '__main__':
    main()
