from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from sqlalchemy.exc import NoResultFound
from typing import List

from models import (
    Base,
    engine,
    session,
    Books,
    Readers,
    ReceivingBooks,
)

app = Flask(__name__)


@app.before_request
def before_request_function() -> None:
    """
    A function creates database tables defined in models.
    It is executed before handling each incoming request.
    It ensures that all tables defined in SQLAlchemy models are
    created in the database. If any table is missing, it will be
    automatically generated.
    """

    Base.metadata.create_all(engine)


@app.route("/books", methods=["GET"])
def get_all_books() -> tuple:
    """A function returns tuple of JSON with existing books
    in the source database and HTTP response status code."""

    all_books: List[Books] = session.query(Books).all()
    if all_books:
        books_json: List[dict] = [book.to_json() for book in all_books]
        return jsonify(books_json), 200
    return "No books in library", 404


@app.route("/books/delinquent_readers", methods=["GET"])
def get_delinquent_readers() -> tuple:
    """
    Endpoint for retrieving a list of delinquent readers who have books
    for more than 14 days.
    :returns: a JSON response containing a list of delinquent readers
    and HTTP response status code.
    """

    try:
        # Calculate the date 14 days ago from the current date:
        fourteen_days_ago_date = datetime.now() - timedelta(days=14)

        # Query the 'receiving_books table' to find records
        # where 'date_of_issue' is more than 14 days ago:
        delinquent_records = session.query(ReceivingBooks).filter(
            ReceivingBooks.date_of_issue <= fourteen_days_ago_date,
            ReceivingBooks.date_of_return == None,
        ).all()

        if not delinquent_records:
            return "No delinquent readers found", 404

        # Collect the list of delinquent readers:
        delinquent_readers = []
        for record in delinquent_records:

            reader = session.query(Readers).filter_by(
                reader_id=record.student_id,
            ).first()

            if reader:
                delinquent_readers.append(
                    {
                        "reader_id": reader.reader_id,
                        "name": reader.name,
                        "surname": reader.surname,
                        "book_id": record.book_id,
                        "days_overdue": (
                                datetime.now() - record.date_of_issue
                        ).days,
                    }
                )

        return jsonify(delinquent_readers), 200

    except Exception as exc:
        return str(exc), 500


@app.route("/books/issuing_book", methods=["POST"])
def issue_book_to_student() -> tuple:
    """
    Endpoint for issuing a book to a student.
    This endpoint receives a JSON request containing 'book_id' and
    'student_id'. It checks the existence of the book and of the
    student in the source database. If all conditions are met, the book's
    count is updated and a new record is added to the 'receiving_books' table.
    :returns: if successful, returns a message indicating the book issuance.
    If any error occurs, returns an appropriate error message and status code.
    """

    try:
        data = request.json
        book_id = data.get("book_id")
        student_id = data.get("student_id")

        if book_id is None or student_id is None:
            return "Fields 'book_id' and 'students_id' are required", 404

        # Check if the book exists in the source DB:
        try:
            book = session.query(Books).filter_by(book_id=book_id).one()
        except NoResultFound:
            return "Book not found", 404

        # Check if the student exists in the source DB:
        try:
            student = session.query(Readers).filter_by(reader_id=student_id).one()
        except NoResultFound:
            return "Student not found", 404

        # Check if the book is available:
        if book.count <= 0:
            return "Book not available", 400

        # Update the book count and create a new
        # record in 'receiving_books' table:
        book.count -= 1
        new_record = ReceivingBooks(
            book_id=book_id,
            student_id=student_id,
            date_of_issue=datetime.now(),
            date_of_return=None,
        )
        session.add(new_record)
        session.commit()

        return f"Book '{book.name}' issued to student '{student.name}'", 200

    except Exception as exc:
        session.rollback()
        return str(exc), 500


@app.route("/books/submitting_book", methods=["POST"])
def submit_book_to_library() -> tuple:
    """
    Endpoint for submitting a book to the library by a student.
    This endpoint receives a JSON request containing 'book_id' and
    'student_id'. It checks that this record exists in the source database.
    If it is, the 'count' in 'books' table and 'date_of_return' in
    'receiving_books' are updated.
    :returns: if successful, returns a message indicating the book submitting.
    If any error occurs, returns an appropriate error message and status code.
    """

    try:
        data = request.json
        book_id = data.get("book_id")
        student_id = data.get("student_id")

        if book_id is None or student_id is None:
            return "Fields 'book_id' and 'students_id' are required", 404

        # Check if the specified record exists in 'receiving_books' table:
        try:
            receiving_book = session.query(ReceivingBooks).filter_by(
                book_id=book_id,
                student_id=student_id,
                date_of_return=None,
            ).one()
        except NoResultFound:
            return "This student doesn't have this book now", 404

        # Update the return date in the 'receiving_books' table:
        receiving_book.date_of_return = datetime.now()
        session.commit()

        # Increase the count of the returned book in the 'books' table:
        try:
            book = session.query(Books).filter_by(book_id=book_id).one()
            book.count += 1
            session.commit()
        except NoResultFound:
            session.rollback()
            return "Book not found", 404

        return f"Book '{book.name}' returned by student with ID {student_id}", 200

    except Exception as exc:
        session.rollback()
        return str(exc), 500


@app.route("/books/searching_by_title", methods=["GET"])
def search_books_by_title() -> tuple:
    """
    Endpoint for searching books by title.
    This endpoint receives a query parameter 'title'
    and returns a JSON response containing a list of
    books whose titles contain the specified keyword.
    :returns: a JSON response with a list of matching
    books and HTTP status code.
    """

    try:
        title = request.args.get("title")

        if title is None:
            return "Field 'title' is required", 404

        # Query the 'books' table to find books
        # with titles containing the keyword:
        matching_books = session.query(Books).filter(
            Books.name.like(f"%{title}%"),
        ).all()

        if not matching_books:
            return "No matching books found", 404

        # Convert matching books to JSON format:
        matching_books_json = [book.to_json() for book in matching_books]

        return jsonify(matching_books_json), 200

    except Exception as exc:
        return str(exc), 500


if __name__ == "__main__":
    app.run(debug=True)
