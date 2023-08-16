from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError
from typing import Optional, List

from models import (
    Book,
    Author,
    DATA,
    get_all_books,
    get_book_by_id,
    init_db,
    add_book,
    update_book_by_id,
    delete_book_by_id,
    get_author_by_id,
    get_all_books_by_author_id,
    delete_author_by_author_id,
    add_author,
)
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    @staticmethod
    def get() -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    @staticmethod
    def post() -> tuple[dict, int]:
        data = request.json
        schema = BookSchema()
        try:
            book: Book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        if 'author' in data:
            author_data = data['author']
            schema = AuthorSchema()
            try:
                author: Author = schema.load(author_data)
            except ValidationError as exc:
                return exc.messages, 400

            author = add_author(author)
            book.author_id = author.id

        book = add_book(book)
        return schema.dump(book), 201


class SelectedBook(Resource):
    @staticmethod
    def get(book_id: int) -> tuple[dict, int]:
        book = get_book_by_id(book_id)
        if book:
            schema = BookSchema()
            return schema.dump(book), 200
        return {"message": "Book not found"}, 404

    @staticmethod
    def put(book_id: int):
        data = request.json
        schema = BookSchema()

        try:
            book_for_updating = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        existing_book: Optional[Book] = get_book_by_id(book_id)
        if not existing_book:
            return {"message": "Book not found"}, 404

        existing_book.title = book_for_updating.title
        existing_book.author_id = book_for_updating.author_id

        update_book_by_id(existing_book)
        return schema.dump(existing_book), 200

    @staticmethod
    def delete(book_id: int) -> tuple[dict, int]:
        book = get_book_by_id(book_id)
        if book:
            delete_book_by_id(book_id)
            return {"message": "Book was successfully deleted"}, 200
        return {"message": "Book not found"}, 404


class SelectedAuthor(Resource):
    @staticmethod
    def post():
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(author)
        return schema.dump(author), 201

    @staticmethod
    def get(author_id: int) -> tuple[dict, int]:
        books: Optional[List[Book]] = get_all_books_by_author_id(author_id)
        if books:
            schema = BookSchema()
            return schema.dump(books, many=True), 200
        return {"message": "Books not found"}, 404

    @staticmethod
    def delete(author_id: int):
        author = get_author_by_id(author_id)
        if author:
            delete_author_by_author_id(author_id)
            return {"message": "Author was successfully deleted"}, 200
        return {"message": "Author not found"}, 404


api.add_resource(BookList, '/api/books')
api.add_resource(SelectedBook, '/api/books/<int:book_id>')
api.add_resource(
    SelectedAuthor,
    '/api/authors',
    '/api/authors/<int:author_id>',
)


if __name__ == '__main__':
    init_db(initial_records=DATA)
    app.run(debug=True)
