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

    draw_result: List[tuple] = []

    # Get command numbers from database by each level:
    for level in ("Top", "Normal", "Weak"):
        command_numbers = cursor.execute("""
            SELECT command_number
                FROM `uefa_commands`
                WHERE command_level = ?;
        """, (level, )).fetchall()

        # Shuffle teams:
        if level == "Normal":
            shuffled_command_numbers = sample(
                command_numbers, number_of_groups * 2
            )
        else:
            shuffled_command_numbers = sample(command_numbers, number_of_groups)

        # Make draw:
        group_number = 0
        current_level_teams = []
        for number in shuffled_command_numbers:
            current_level_teams.append((*number, group_number % number_of_groups + 1))
            group_number += 1
        draw_result.extend(current_level_teams)

    # Fill 'uefa_draw' table with result of the draw:
    cursor.executemany("""
        INSERT INTO `uefa_draw`
            (command_number, group_number)
            VALUES (?, ?);
    """, draw_result)


def main() -> None:
    """The main function of the app."""

    number_of_groups = int(input('Введите количество групп (от 4 до 16): '))

    if number_of_groups not in range(4, 17):
        print("Вы ввели неверное количество групп.")
        return

    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        generate_test_data(cursor, number_of_groups)
        conn.commit()


if __name__ == '__main__':
    main()
