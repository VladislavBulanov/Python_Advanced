from flask import Flask
from re import match

app = Flask(__name__)

storage = {}
months = (
    'январь',
    'февраль',
    'март',
    'апрель',
    'май',
    'июнь',
    'июль',
    'август',
    'сентябрь',
    'октябрь',
    'ноябрь',
    'декабрь',
)


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int) -> str:
    """
    The function saves information about the expenses in specified date.
    :param date: the date when the expenses were made
    :param number: amount of expenses
    """
    if match(r'^\d{4}[0-1][0-9][0-3][0-9]$', date):
        year = date[0:4]
        month = date[5] if date[4] == '0' else date[4:6]
        day = date[7] if date[6] == '0' else date[6:]
        storage.setdefault(year, dict()).setdefault(month, dict())
        storage[year][month].setdefault(day, 0)
        storage[year][month][day] += number
        storage[year][month].setdefault('total', 0)
        storage[year][month]['total'] += number
        storage[year].setdefault('total', 0)
        storage[year]['total'] += number
        return 'Запись успешно сохранена в базе данных!'

    return 'Введённая дата не соответствует формату "YYYYMMDD".'


@app.route("/calculate/<int:year>")
def calculate_year(year: int) -> str:
    """
    The function returns total expenses for the specified year.
    :param year: source year
    """
    if not 1000 <= year <= 9999:
        return 'Введённый год не соответствует формату "YYYY".'

    try:
        amount = storage[str(year)]['total']
    except KeyError:
        amount = 0
    return f'Суммарные траты за {year}-й год составляют <b>{amount}</b> руб.'


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int) -> str:
    """
    The function returns total expenses for the
    specified month of the specified year.
    :param year: source year
    :param month: source month
    """
    if (not 1000 <= year <= 9999) or (not 1 <= month <= 12):
        return 'Некорректное значение года и/или месяца.'

    try:
        amount = storage[str(year)][str(month)]['total']
    except KeyError:
        amount = 0
    return (f'Суммарные траты за {months[month - 1]} {year}-го года '
            f'составляют <b>{amount}</b> руб.')


@app.route('/show_db')
def show_db() -> dict:
    """Test function to show current database."""
    return storage


if __name__ == "__main__":
    app.run(debug=True)
