import os
from datetime import datetime, timedelta
from typing import List, Optional
from random import choice
from re import findall
from flask import Flask


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')
BOOKS_WORDS: List[str] = []
TOTAL_PAGES_VISITS = 0

cars: List[str] = ['Chevrolet', 'Renault', 'Ford', 'Lada']
cats: List[str] = [
    'Корниш-рекс',
    'Русская голубая',
    'Шотландская вислоухая',
    'Мейн-кун',
    'Манчкин',
]


@app.route('/hello_world')
def get_hello_world_page():
    return 'Привет, мир!'


@app.route('/cars')
def show_list_of_cars():
    return ', '.join(cars)


@app.route('/cats')
def get_cats_breed():
    return choice(cats)


@app.route('/get_time/now')
def get_current_time():
    current_time = datetime.now()
    return 'Точное время: {time}'.format(
        time=current_time,
    )


@app.route('/get_time/future')
def get_time_after_hour():
    current_time_after_hour = datetime.now() + timedelta(hours=1)
    return 'Точное время через час будет {time}'.format(
        time=current_time_after_hour,
    )


@app.route('/get_random_word')
def get_random_word():
    global BOOKS_WORDS
    if not BOOKS_WORDS:
        BOOKS_WORDS = get_words_from_file(BOOK_FILE)
    return choice(BOOKS_WORDS)


@app.route('/counter')
def get_total_visits():
    global TOTAL_PAGES_VISITS
    TOTAL_PAGES_VISITS += 1
    return str(TOTAL_PAGES_VISITS)


def get_words_from_file(file_path: str) -> Optional[List[str]]:
    """
    The function returns list of words from source file.
    If source file doesn't exist function print error message
    and returns None.
    :param file_path: path to source file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            return findall(r'\b\w+\b', text)
    except FileNotFoundError:
        print('Файл по указанному пути не существует.')


if __name__ == '__main__':
    app.run(debug=True)
