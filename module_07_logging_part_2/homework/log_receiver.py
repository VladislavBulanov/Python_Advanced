"""A module with Flask app which runs
server for receiving and getting logs."""

import json
from flask import Flask, request
from typing import List


app = Flask(__name__)
_logs: List[dict] = []


@app.route('/receive_log', methods=['POST'])
def receive_log():
    """The function receive log and add him to list of logs."""

    _logs.append(dict(request.form))
    return 'The log was successfully registered', 200


@app.route('/get_logs', methods=['GET'])
def get_logs() -> str:
    """The function allows the user to get registered logs."""

    logs_list: list[str] = list(
        map(lambda log: json.dumps(log, indent=4), _logs)
    )
    logs_text: str = '\n'.join(logs_list)
    return f'<pre>{logs_text}</pre>'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3080, debug=True)
