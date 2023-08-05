import sqlite3


SQL_SCRIPT: str = """
    PRAGMA foreign_keys = ON;
    
    DROP TABLE IF EXISTS `director`;
    CREATE TABLE `director`(
        dir_id INTEGER PRIMARY KEY AUTOINCREMENT,
        dir_first_name VARCHAR(50) NOT NULL,
        dir_last_name VARCHAR(50) NOT NULL
    );
    
    DROP TABLE IF EXISTS `movie`;
    CREATE TABLE `movie`(
        mov_id INTEGER PRIMARY KEY AUTOINCREMENT,
        mov_title VARCHAR(50) NOT NULL
    );
    
    DROP TABLE IF EXISTS `actors`;
    CREATE TABLE `actors`(
        act_id INTEGER PRIMARY KEY AUTOINCREMENT,
        act_first_name VARCHAR(50) NOT NULL,
        act_last_name VARCHAR(50) NOT NULL,
        act_gender VARCHAR(1) NOT NULL
    );
    
    DROP TABLE IF EXISTS `movie_direction`;
    CREATE TABLE `movie_direction`(
        dir_id INTEGER NOT NULL,
        mov_id INTEGER NOT NULL,
        FOREIGN KEY(dir_id) REFERENCES `director`(dir_id) ON DELETE CASCADE,
        FOREIGN KEY(mov_id) REFERENCES `movie`(mov_id) ON DELETE CASCADE
    );
    
    DROP TABLE IF EXISTS `oscar_awarded`;
    CREATE TABLE `oscar_awarded`(
        award_id INTEGER PRIMARY KEY AUTOINCREMENT,
        mov_id INTEGER NOT NULL,
        FOREIGN KEY(mov_id) REFERENCES `movie`(mov_id) ON DELETE CASCADE
    );
    
    DROP TABLE IF EXISTS `movie_cast`;
    CREATE TABLE `movie_cast`(
        act_id INTEGER NOT NULL,
        mov_id INTEGER NOT NULL,
        role VARCHAR(50) NOT NULL,
        FOREIGN KEY(act_id) REFERENCES `actors`(act_id) ON DELETE CASCADE,
        FOREIGN KEY(mov_id) REFERENCES `movie`(mov_id) ON DELETE CASCADE
    );
"""


with sqlite3.connect("film_database.db") as conn:
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.executescript(SQL_SCRIPT)
    conn.commit()
