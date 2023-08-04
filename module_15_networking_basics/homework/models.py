"""A module consists of two models: a model of the hotel room
and a model of the hotel room booking and also the functions
for interaction with source database."""


import sqlite3
from typing import List


DB_NAME: str = "hotels.db"


class Room:
    """A model of the hotel room."""

    def __init__(
            self,
            room_id: int,
            floor: int,
            beds: int,
            guest_num: int,
            price: int,
    ) -> None:
        """The class constructor."""

        self.room_id = room_id
        self.floor = floor
        self.beds = beds
        self.guest_num = guest_num
        self.price = price


class Booking:
    """A model of the hotel room booking."""

    def __init__(
            self,
            check_in: str,
            check_out: str,
            first_name: str,
            last_name: str,
            room_id: int,
    ) -> None:
        """The class constructor."""

        self.check_in = check_in
        self.check_out = check_out
        self.first_name = first_name
        self.last_name = last_name
        self.room_id = room_id


def create_tables() -> None:
    """A function creates tables in source database."""

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS `rooms` (
                room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                floor INTEGER NOT NULL,
                beds INTEGER NOT NULL,
                guest_num INTEGER NOT NULL,
                price INTEGER NOT NULL
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS `bookings` (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                check_in TEXT NOT NULL,
                check_out TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                room_id INTEGER NOT NULL,
                FOREIGN KEY (room_id) REFERENCES `rooms` (room_id)
            );
            """
        )


def insert_room(room: Room) -> int:
    """
    A function adds room information in database
    and returns ID of the last added room.
    :param room: the instance of "Room" class
    """

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO `rooms` (floor, beds, guest_num, price)
            VALUES (?, ?, ?, ?);
            """,
            (room.floor, room.beds, room.guest_num, room.price)
        )

        # Get the ID of the inserted room:
        room_id = cursor.lastrowid
        conn.commit()

    return room_id


def get_rooms() -> List[Room]:
    """A function returns all hotel rooms from source database."""

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM `rooms`;")
        data = cursor.fetchall()

        # Create "Room" objects for each row of data and add them to the list:
        rooms = []
        for row in data:
            room = Room(
                room_id=row[0],
                floor=row[1],
                beds=row[2],
                guest_num=row[3],
                price=row[4],
            )
            rooms.append(room)

    return rooms


def is_room_booked(
        room_id: int,
        check_in: str,
        check_out: str,
) -> bool:
    """
    A function returns True if the source room is booked for
    specified period. Otherwise, a function returns False.
    :param room_id: the ID of the source hotel room
    :param check_in: the date of check in
    :param check_out: the date of check out
    """

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM `bookings`
            WHERE room_id = ? AND (check_in < ? AND check_out > ?);
            """,
            (
                room_id,
                check_out,
                check_in,
            )
        )
        return cursor.fetchone()[0] > 0


def insert_booking(booking: Booking) -> None:
    """
    A function inserts booking information into source database.
    :param booking: the source instance of "Booking" class
    """

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO `bookings` (
                check_in,
                check_out,
                first_name,
                last_name,
                room_id
            )
            VALUES (?, ?, ?, ?, ?);
            """,
            (
                booking.check_in,
                booking.check_out,
                booking.first_name,
                booking.last_name,
                booking.room_id,
            )
        )

        # Remove the booked room from the `rooms` table:
        cursor.execute(
            """
            DELETE FROM `rooms`
            WHERE room_id = ?;
            """,
            (booking.room_id, )
        )

        conn.commit()
