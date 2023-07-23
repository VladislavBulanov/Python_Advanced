from flask import Flask, render_template, request, redirect, url_for
from requests import Response
from typing import Union, List

from models import init_db, get_all_books, add_book, DATA

app: Flask = Flask(__name__)


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
    if request.method == "POST":
        title = request.form["book_title"]
        author = request.form["author_name"]
        add_book(title, author)
        return redirect(url_for("all_books"))

    return render_template('add_book.html')


if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
