from flask import Flask


app = Flask(__name__)


@app.route("/max_number/<path:numbers>")
def max_number(numbers: str) -> str:
    """
    The function receives string with numbers to compare (any quantity
    but at least one) and returns message with the max one of them.
    :param numbers: string with numbers to compare
    """
    try:
        numbers_list = [int(number) for number in numbers.split('/')]
        maximum_number = max(numbers_list)
        return f'Максимальное число: {maximum_number}'
    except ValueError:
        return 'В URL передано не число.'


if __name__ == "__main__":
    app.run(debug=True)
