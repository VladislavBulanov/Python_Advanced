from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from requests import Response
from typing import Union, List
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

from models import init_db, get_all_books, retrieve_books_by_author, add_book, DATA

app: Flask = Flask(__name__)
app.config['SECRET_KEY'] = "sample_key"


class NewBookRegistrationForm(FlaskForm):
    """A child class of 'FlaskForm' class
    describing new book registration form."""

    book_title = StringField(validators=[
        InputRequired(message="The field 'title' is required"),
    ])
    author_name = StringField(validators=[
        InputRequired(message="The field 'author' is required"),
    ])
    submit = SubmitField("Add new book")


def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
        <table>
            <thead>
            <tr>
                <th>ID</td>
                <th>Title</td>
                <th>Author</td>
            </tr>
            </thead>
            <tbody>
                {books_rows}
            </tbody>
        </table>
    """
    rows: str = ''
    for book in books:
        rows += '<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>'.format(
            id=book['id'], title=book['title'], author=book['author'],
        )
    return table.format(books_rows=rows)


@app.route('/books')
def all_books() -> str:
    return render_template(
        'index.html',
        books=get_all_books(),
    )


@app.route('/books/form', methods=["GET", "POST"])
def get_books_form() -> Union[str, Response]:
    book_form = NewBookRegistrationForm()

    if book_form.validate_on_submit():
        title = book_form.book_title.data
        author = book_form.author_name.data
        add_book(title, author)
        return redirect(url_for("all_books"))

    return render_template('add_book.html', form=book_form)


@app.route("/books/<string:author>")
def get_books_by_author(author: str) -> str:
    """
    The function returns HTML-page with the table of books
    from the source database written by specified author.
    :param author: the source author
    """

    return render_template(
        'books_by_author.html',
        books=retrieve_books_by_author(author),
    )


if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
