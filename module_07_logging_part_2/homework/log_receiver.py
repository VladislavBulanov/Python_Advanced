"""A module with Flask app which runs server for creating log receiver."""

import logging.config
from flask import Flask, request, jsonify

from logging_config import dict_config


app = Flask(__name__)
logs = []


@app.route('/log_receiver', methods=['POST'])
def receive_logs():
    log = request.get_json()
    logs.append(log)
    return jsonify({'message': 'Log received'})


@app.route('/log_receiver', methods=['GET'])
def get_logs():
    return jsonify(logs)


if __name__ == '__main__':
    logging.config.dictConfig(dict_config)
    app.run(debug=True)
