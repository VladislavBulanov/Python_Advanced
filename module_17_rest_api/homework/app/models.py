import sqlite3
from dataclasses import dataclass
from typing import Union, Optional, List, Dict


DATA = [
    {
        'id': 0,
        'title': 'A Byte of Python',
        'author_id': 1,
        'first_name': None,
        'last_name': 'Swaroop C. H.',
        'middle_name': None,
    },
    {
        'id': 1,
        'title': 'Moby-Dick; or, The Whale',
        'author_id': 2,
        'first_name': 'Herman',
        'last_name': 'Melville',
        'middle_name': None,
    },
    {
        'id': 3,
        'title': 'War and Peace',
        'author_id': 3,
        'first_name': 'Lev',
        'last_name': 'Tolstoy',
        'middle_name': 'Nikolaevich',
    },
]

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'


@dataclass
class Author:
    """A dataclass describes the author."""

    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None


@dataclass
class Book:
    """A dataclass describes the book."""

    title: str
    author_id: int
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def init_db(initial_records: List[Dict]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{BOOKS_TABLE_NAME}';
            """
        )
        exists = cursor.fetchone()

        if not exists:
            cursor.executescript(
                f"""
                PRAGMA foreign_keys = ON;
                
                CREATE TABLE `{BOOKS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT,
                    author_id INTEGER,
                    FOREIGN KEY(author_id) REFERENCES `authors`(id) ON DELETE CASCADE
                );
                
                CREATE TABLE `authors`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    last_name TEXT,
                    middle_name TEXT
                );
                """
            )

            cursor.executemany(
                f"""
                INSERT INTO `authors`
                (first_name, last_name, middle_name) VALUES (?, ?, ?)
                """,
                [
                    (
                        item['first_name'],
                        item['last_name'],
                        item['middle_name'],
                    )
                    for item in initial_records
                ]
            )

            cursor.executemany(
                f"""
                INSERT INTO `{BOOKS_TABLE_NAME}`
                (title, author_id) VALUES (?, ?)
                """,
                [
                    (item['title'], item['author_id'])
                    for item in initial_records
                ]
            )


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0], title=row[1], author_id=row[2])


def _get_author_obj_from_row(row: tuple) -> Author:
    return Author(
        id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3],
    )


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` 
            (title, author_id) VALUES (?, ?)
            """,
            (book.title, book.author_id)
        )
        book.id = cursor.lastrowid
        return book


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}`
            WHERE id = ?;
            """,
            (book_id, )
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {BOOKS_TABLE_NAME}
            SET title = ?, author_id = ?
            WHERE id = ?;
            """,
            (book.title, book.author_id, book.id)
        )
        conn.commit()


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE id = ?;
            """,
            (book_id, )
        )
        conn.commit()


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}`
            WHERE title = ?;
            """,
            (book_title, )
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def get_author_by_id(author_id: int) -> Optional[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM `authors`
            WHERE id = ?;
            """,
            (author_id, )
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)


def get_all_books_by_author_id(author_id: int) -> Optional[List[Book]]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}`
            WHERE author_id = ?;
            """,
            (author_id, )
        )
        books = cursor.fetchall()
        if books:
            return [_get_book_obj_from_row(row) for row in books]


def delete_author_by_author_id(author_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.executescript(
            f"""
            PRAGMA foreign_keys = ON;
            
            DELETE FROM `authors`
            WHERE id = {author_id};
            """
        )
        conn.commit()


def add_author(author: Author) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO `authors`
            (first_name, last_name, middle_name)
            VALUES (?, ?, ?)
            """,
            (author.first_name, author.last_name, author.middle_name)
        )
        author.id = cursor.lastrowid
        return author


def get_author_by_full_name(
        first_name: str,
        middle_name: Optional[str],
        last_name: str,
) -> Optional[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        if middle_name:
            cursor.execute(
                """
                SELECT * FROM `authors`
                WHERE first_name = ?
                AND middle_name = ?
                AND last_name = ?;
                """,
                (first_name, middle_name, last_name)
            )
        else:
            cursor.execute(
                """
                SELECT * FROM `authors`
                WHERE first_name = ?
                AND middle_name IS NULL
                AND last_name = ?;
                """,
                (first_name, last_name)
            )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)
