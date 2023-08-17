from flasgger import Schema, fields, ValidationError
from marshmallow import validates, post_load
from typing import Optional

from models import (
    get_book_by_title,
    get_author_by_id,
    get_author_by_full_name,
    Book,
    Author,
)


class AuthorSchema(Schema):
    """Schema for validating and serializing author data."""

    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str(required=False)

    @post_load
    def create_author(self, data: dict, **kwargs) -> Author:
        """
        Create an Author instance after validation.
        :param data: validated author data
        :return: created 'Author' class instance
        :raise ValidationError: if the author
        with the same name already exists
        """

        is_author_exist: Optional[Author] = get_author_by_full_name(
            data.get('first_name'),
            data.get('middle_name', None),
            data.get('last_name'),
        )
        if is_author_exist:
            raise ValidationError('This author already exists in database')
        return Author(**data)


class BookSchema(Schema):
    """Schema for validating and serializing book data."""

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author_id = fields.Int(required=True, allow_none=True)
    author = fields.Nested(AuthorSchema, required=False)

    @validates('title')
    def validate_title(self, title: str) -> None:
        """
        Validate the uniqueness of the book title.
        :param title: the book title
        :return: None
        :raise ValidationError: if a book with the same title already exists
        """

        if get_book_by_title(title) is not None:
            raise ValidationError(
                'Book with title "{title}" already exists, '
                'please use a different title.'.format(title=title)
            )

    @validates('author_id')
    def validate_author_id(self, author_id: int) -> None:
        """
        Validate the existence of the author with the provided ID.
        :param author_id: the author ID
        :return: none
        :raise ValidationError: if the author with the given ID does not exist
        """

        if author_id is not None and get_author_by_id(author_id) is None:
            raise ValidationError(
                'Author with this ID does not exist in database'
            )

    @post_load
    def create_book(self, data: dict, **kwargs) -> Book:
        """
        Create a Book instance after validation.
        :param data: validated book data
        :return: created 'Book' class instance
        """

        if 'author' in data:
            data.pop('author')
        return Book(**data)
