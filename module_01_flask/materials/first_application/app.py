import datetime
from flask import Flask


app = Flask(__name__)
total_calls = 0


@app.route('/test')
def test_function():
    now = datetime.datetime.now().utcnow()
    return f'Это тестовая страничка, ответ сгенерирован в {now}'


@app.route('/hello/world')
def print_hello_world():
    return 'Hello, world!'


@app.route('/counter')
def show_total_calls():
    global total_calls
    total_calls += 1
    return str(total_calls)
