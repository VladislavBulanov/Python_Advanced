import logging
import requests
import sqlite3
import time
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
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


def fetch_characters_data_parallel_way_by_pool() -> None:
    """The function makes parallel requests to SWAPI to get the data of
    Star Wars' characters via 'Pool' from 'multiprocessing' module."""

    start_time = time.time()
    logger.info("THE PARALLEL REQUESTS BY POOL FUNCTION IS STARTED")

    with Pool() as pool:
        character_ids = range(1, 16)
        characters = pool.map(get_character_data, character_ids)

    logger.info("All characters are received")

    create_database(characters, "star_wars_parallel_pool.db")

    end_time = time.time()
    performing_time = end_time - start_time
    logger.info(f"Performing time: {round(performing_time, 3)}s")


def fetch_characters_data_parallel_way_by_threadpool() -> None:
    """The function makes parallel requests to SWAPI to get
    the data of Star Wars' characters via 'Pool.ThreadPool'
    from 'multiprocessing' module."""

    start_time = time.time()
    logger.info("THE PARALLEL REQUESTS BY THREADPOOL FUNCTION IS STARTED")

    with ThreadPool() as thread_pool:
        character_ids = range(1, 16)
        characters = thread_pool.map(get_character_data, character_ids)

    logger.info("All characters are received")

    create_database(characters, "star_wars_parallel_threadpool.db")

    end_time = time.time()
    performing_time = end_time - start_time
    logger.info(f"Performing time: {round(performing_time, 3)}s")


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
    Star Wars characters by parallel way via 'Pool' and
    'Pool.ThreadPool' from 'multiprocessing' module."""

    logger.info("=====THE APP IS STARTED=====")
    fetch_characters_data_parallel_way_by_pool()
    fetch_characters_data_parallel_way_by_threadpool()
    logger.info("=====THE APP IS FINISHED=====\n")


if __name__ == "__main__":
    main()
