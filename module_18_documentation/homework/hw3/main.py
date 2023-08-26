import operator
from flask import Flask, jsonify
from flasgger import Swagger
from flask_jsonrpc import JSONRPC

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)
swagger = Swagger(app, template_file="swagger.yaml")


class JSONRPCError(Exception):
    """A class for JSON-RPC errors."""

    def __init__(self, code, message):
        """A class constructor."""
        self.code = code
        self.message = message


@jsonrpc.method('calc.add')
def add(a: float, b: float) -> float:
    """
    The adding two numbers.
    :param a: the first number
    :param b: the second number
    :return: the sum of two numbers
    """
    return operator.add(a, b)


@jsonrpc.method('calc.subtract')
def subtract(a: float, b: float) -> float:
    """
    The subtracting the second number from the first one.
    :param a: the first number
    :param b: the second number
    :return: the difference between two numbers
    """
    return operator.sub(a, b)


@jsonrpc.method('calc.multiply')
def multiply(a: float, b: float) -> float:
    """
    The multiplication of two numbers.
    :param a: the first number
    :param b: the second number
    :return: the multiplication of two numbers
    """
    return operator.mul(a, b)


@jsonrpc.method('calc.divide')
def divide(a: float, b: float) -> float:
    """
    The dividing the first number by the second one.
    :param a: the first number
    :param b: the second number
    :return: the quotient of two numbers
    :raise JSONRPCError: division by zero is not allowed
    """
    if b == 0:
        raise JSONRPCError(-32000, "Division by zero is not allowed")
    return operator.truediv(a, b)


@app.errorhandler(JSONRPCError)
def handle_jsonrpc_error(error):
    """
    JSON-RPC Error Handler.
    This function is used to handle errors of the JSONRPCError type.
    It constructs a JSON response that includes error information,
    including the error code and message.
    :param error: an object of the JSONRPCError type,
    containing information about the occurred error
    :return: a JSON response containing error information
    """

    response = jsonify({
        "jsonrpc": "2.0",
        "error": {
            "code": error.code,
            "message": error.message
        },
        "id": None
    })
    return response, 200


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
