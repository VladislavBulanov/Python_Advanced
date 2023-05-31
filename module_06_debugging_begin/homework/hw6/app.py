from flask import Flask, render_template
from werkzeug.exceptions import NotFound

app = Flask(__name__, template_folder='templates')


@app.route('/dogs')
def dogs():
    return 'Страница с пёсиками'


@app.route('/cats')
def cats():
    return 'Страница с котиками'


@app.route('/cats/<int:cat_id>')
def cat_page(cat_id: int):
    return f'Страница с котиком {cat_id}'


@app.route('/index')
def index():
    return 'Главная страница'


@app.errorhandler(404)
def handle_page_not_found_exception(error: NotFound):
    """The function handles page not found error
    and shows to user existing pages."""

    available_pages = [
        str(rule) for rule in app.url_map.iter_rules()
        if "GET" in rule.methods and "static" not in str(rule)
    ]

    return render_template('error_404.html', urls=available_pages), 404


if __name__ == '__main__':
    app.run(debug=True)
