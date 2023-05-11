import os
from flask import Flask


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__name__))


@app.route("/head_file/<int:size>/<path:relative_path>")
def head_file(size: int, relative_path: str) -> str:
    """
    The function returns absolute path of source file
    and shows specified quantity of starting symbols.
    :param size: quantity of staring symbols of source file
    :param relative_path: relative path to the source file
    """
    abs_path = os.path.join(BASE_DIR, relative_path)
    try:
        with open(abs_path, 'r', encoding='utf-8') as file:
            preview = file.read(size)
        return f'<b>{abs_path}</b> {size}<br>{preview}'

    except FileNotFoundError:
        return 'Неверно указан путь к файлу.'


if __name__ == "__main__":
    app.run(debug=True)
