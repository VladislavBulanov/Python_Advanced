from datetime import datetime
from flask import Flask
from re import match

app = Flask(__name__)

GREETINGS = (
    'Хорошего понедельника',
    'Хорошего вторника',
    'Хорошей среды',
    'Хорошего четверга',
    'Хорошей пятницы',
    'Хорошей субботы',
    'Хорошего воскресенья'
)


@app.route('/hello-world/<name>')
def hello_world(name: str) -> str:
    if not match(r'^\w+$', name):
        return 'Введено некорректное имя'

    weekday: int = datetime.today().weekday()
    greeting: str = GREETINGS[weekday]
    return f'Привет, {name}. {greeting}!'


if __name__ == '__main__':
    app.run(debug=True)
