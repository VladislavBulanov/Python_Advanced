"""A module with SQLAlchemy ORM models."""

from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, Float, String, Date, Boolean, DateTime,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Dict, Any, List


engine = create_engine("sqlite:///library.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Books(Base):
    """A model describes the table of books."""

    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Title: {self.name}, count: {self.count}, " \
               f"release date: {self.release_date}, " \
               f"author ID: {self.author_id}"

    def to_json(self) -> Dict[str, Any]:
        """A method for retrieving data in JSON format."""

        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }


class Authors(Base):
    """A model describes the table of authors."""

    __tablename__ = "authors"

    author_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"Name: {self.name}, surname: {self.surname}"

    def to_json(self) -> Dict[str, Any]:
        """A method for retrieving data in JSON format."""

        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }


class Readers(Base):
    """A model describes the table of readers."""

    __tablename__ = "readers"

    reader_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    def __repr__(self) -> str:
        return f"Name: {self.name}, surname: {self.surname}, " \
               f"phone: {self.phone}, email: {self.email}, " \
               f"average score: {self.average_score}, " \
               f"scholarship: {self.scholarship}"

    def to_json(self) -> Dict[str, Any]:
        """A method for retrieving data in JSON format."""

        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    @classmethod
    def get_students_living_in_dorm(cls) -> List["Readers"]:
        """
        A function returns list of students which live in the dorm.
        :return: the list of 'Readers' class instances
        """

        return session.query(Readers).filter_by(scholarship=1).all()

    @classmethod
    def get_students_with_average_score_higher_than_specified(
            cls,
            score: float,
    ) -> List["Readers"]:
        """
        A function returns list of students which have
        the average score higher than specified.
        :param score: the specified score
        :return: the list of 'Readers' class instances
        """

        return session.query(Readers).filter(Readers.average_score > score).all()


class ReceivingBooks(Base):
    """A model describes the table of receiving books."""

    __tablename__ = "receiving_books"

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)

    def __repr__(self) -> str:
        return f"Book ID: {self.book_id}, " \
               f"student ID: {self.student_id}, " \
               f"date of issue: {self.date_of_issue}, " \
               f"date of return: {self.date_of_return}"

    def to_json(self) -> Dict[str, Any]:
        """A method for retrieving data in JSON format."""

        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    @hybrid_property
    def count_date_with_book(self) -> int:
        """A function returns the quantity of days
        that the reader kept/is keeping book."""

        if self.date_of_return is None:
            return (datetime.now() - self.date_of_issue).days
        else:
            return (self.date_of_return - self.date_of_issue).days
