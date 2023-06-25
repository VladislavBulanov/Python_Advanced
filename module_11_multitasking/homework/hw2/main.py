import logging
import requests
import sqlite3
import time
import threading
from typing import List


API_URL = "https://swapi.dev/api/people/"

logging.basicConfig(
    level="INFO",
    filename="logs.log",
    filemode="a",
    format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s',
    datefmt='%H:%M:%S',
)
logger: logging.Logger = logging.getLogger(__name__)


def get_character_data(char_id: int) -> dict:
    """
    The function makes requests to SWAPI and returns
    the dictionary with data of Star Wars' character.
    :param char_id: the ID of Star Wars' character in SWAPI database
    :raise Exception: if status code of response not is 200
    """

    response = requests.get(f"{API_URL}{str(char_id)}")

    if response.status_code != 200:
        logger.error(
            f"Status code: {response.status_code}, "
            f"character ID №{char_id}"
        )
        raise Exception(f"Something's wrong, status code: {response.status_code}")

    data = response.json()
    character = {
        "name": data.get("name", 0),
        "age": data.get("birth_year", 0),
        "gender": data.get("gender", 0),
    }
    return character


def fetch_characters_data_sequential() -> None:
    """The function makes sequential requests to SWAPI
    to get the data of Star Wars' characters."""

    start_time = time.time()
    logger.info("THE SEQUENTIAL REQUESTS FUNCTION IS STARTED")
    characters: List[dict] = []

    for char_id in range(1, 16):
        character = get_character_data(char_id)
        characters.append(character)
    logger.info("All characters are received")

    create_database(characters, "star_wars_sequential.db")

    end_time = time.time()
    performing_time = end_time - start_time
    logger.info(f"Performing time: {round(performing_time, 3)}s")


def fetch_characters_data_parallel() -> None:
    """The function makes parallel requests to SWAPI
    to get the data of Star Wars' characters."""

    start_time = time.time()
    logger.info("THE PARALLEL REQUESTS FUNCTION IS STARTED")
    characters: List[dict] = []

    # Create a pool of threads:
    threads: list[threading.Thread] = []

    def get_and_append_character_data(char_number: int) -> None:
        nonlocal characters
        character = get_character_data(char_number)
        characters.append(character)

    # Start the threads for each character:
    for char_id in range(1, 16):
        thread = threading.Thread(
            target=get_and_append_character_data,
            args=(char_id,),
        )
        thread.start()
        threads.append(thread)

    # Waiting for completion of all threads:
    for thread in threads:
        thread.join()

    logger.info("All characters are received")

    create_database(characters, "star_wars_parallel.db")

    end_time = time.time()
    performing_time = end_time - start_time
    logger.info(f"Performing time: {round(performing_time, 3)}s")


def create_database(characters: List[dict], db_name: str) -> None:
    """
    The function creates database of Star Wars characters
    and insert the characters' information.
    :param characters: the list of dictionaries with data of characters
    :param db_name: the name of created database
    """

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age TEXT,
                gender TEXT
            )
        '''
        cursor.execute(create_table_query)

        for character in characters:
            name = character['name']
            age = character['age']
            gender = character['gender']
            insert_query = "INSERT INTO characters (name, age, gender) VALUES (?, ?, ?)"
            cursor.execute(insert_query, (name, age, gender))

        conn.commit()
    logger.info(f"Database '{db_name}' is created")


def main() -> None:
    """The main function of app. We get the data about
    Star Wars characters by sequential and parallel ways."""

    logger.info("=====THE APP IS STARTED=====")
    fetch_characters_data_sequential()
    fetch_characters_data_parallel()
    logger.info("=====THE APP IS FINISHED=====")


if __name__ == "__main__":
    main()
