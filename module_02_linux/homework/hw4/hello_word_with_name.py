from datetime import datetime, timedelta
from flask import Flask


app = Flask(__name__)


@app.route('/hello-world/<string:name>')
def hello_world(name: str) -> str:
    """Returns a personal greeting on the current day of the week."""
    weekdays_tuple = (
        'понедельника',
        'вторника',
        'среды',
        'четверга',
        'пятницы',
        'субботы',
        'воскресенья',
    )
    current_weekday = (datetime.today() + timedelta()).weekday()  # Timedelta for testing
    ending = 'го' if current_weekday in (0, 1, 3, 6) else 'й'
    return f'Привет, {name}. Хороше{ending} {weekdays_tuple[current_weekday]}!'


if __name__ == '__main__':
    app.run(debug=True)
