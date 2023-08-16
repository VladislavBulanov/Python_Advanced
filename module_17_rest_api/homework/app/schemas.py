from marshmallow import Schema, fields, validates, ValidationError, post_load
from typing import Optional

from models import (
    get_book_by_title,
    get_author_by_id,
    get_author_by_full_name,
    Book,
    Author,
)


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str(required=False)

    @post_load
    def create_author(self, data: dict, **kwargs) -> Author:
        is_author_exist: Optional[Author] = get_author_by_full_name(
            data.get('first_name'),
            data.get('middle_name', None),
            data.get('last_name'),
        )
        if is_author_exist:
            raise ValidationError('This author already exists in database')
        return Author(**data)


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author_id = fields.Int(required=True, allow_none=True)
    author = fields.Nested(AuthorSchema, required=False)

    @validates('title')
    def validate_title(self, title: str) -> None:
        if get_book_by_title(title) is not None:
            raise ValidationError(
                'Book with title "{title}" already exists, '
                'please use a different title.'.format(title=title)
            )

    @validates('author_id')
    def validate_author_id(self, author_id: int) -> None:
        if author_id is not None and get_author_by_id(author_id) is None:
            raise ValidationError(
                'Author with this ID does not exist in database'
            )

    @post_load
    def create_book(self, data: dict, **kwargs) -> Book:
        if 'author' in data:
            data.pop('author')
        return Book(**data)
