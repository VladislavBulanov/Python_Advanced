import sqlite3
from typing import Union, Optional, Any, List

DATA: List[dict] = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.', 'views': 0},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville', 'views': 0},
    {'id': 2, 'title': 'War and Peace', 'author': 'Leo Tolstoy', 'views': 0},
]


class Book:
    """A class for describing book."""

    def __init__(self, id: int, title: str, author: str, views: int) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.views: int = views

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_books'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `table_books` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, 
                    author TEXT,
                    views INTEGER
                );
                """
            )
            cursor.executemany(
                """
                INSERT INTO `table_books`
                (title, author, views) VALUES (?, ?, ?);
                """,
                [
                    (item['title'], item['author'], item['views'])
                    for item in initial_records
                ]
            )


def get_all_books() -> List[Book]:
    """
    The function returns the list of 'Book' class instances
    which are created on data from the source database.
    """

    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE `table_books`
            SET views = views + ?;
            """,
            (1, )
        )
        cursor.execute(
            """
            SELECT * from `table_books`;
            """
        )
        return [Book(*row) for row in cursor.fetchall()]


def retrieve_books_by_author(author: str) -> List[Book]:
    """
    The function returns the list of 'Book' class instances.
    The books belong to the specified author.
    :param author: the source author
    """

    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE `table_books`
            SET views = views + ?
            WHERE author = ?;
            """,
            (1, author)
        )
        cursor.execute(
            """
            SELECT * from `table_books`
            WHERE author = ?;
            """,
            (author, )
        )
        return [Book(*row) for row in cursor.fetchall()]


def retrieve_book_by_id(book_id: int) -> Union[Book, False]:
    """
    The function returns the 'Book' class instance
    if the book with source ID exists in database.
    Otherwise, the function returns False.
    :param book_id: the ID of the source book in database
    """

    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE `table_books`
            SET views = views + ?
            WHERE id = ?;
            """,
            (1, book_id)
        )
        cursor.execute(
            """
            SELECT * from `table_books`
            WHERE id = ?;
            """,
            (book_id, )
        )
        result = cursor.fetchone()
        return Book(*result) if result else False


def add_book(title: str, author: str) -> None:
    """
    The function adds a book with specified title and author in database.
    :param title: the title of the book
    :param author: the author of the book
    """

    with sqlite3.connect("table_books.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO `table_books` (title, author, views)
            VALUES (?, ?, ?);
            """,
            (title, author, 0)
        )
        conn.commit()
