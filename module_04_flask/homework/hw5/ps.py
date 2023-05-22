import shlex

from flask import Flask, request
from subprocess import run, PIPE
from typing import List


app = Flask(__name__)


@app.route('/ps', methods=['GET'])
def execute_ps() -> str:
    """The function returns result of performing 'ps' command with arguments."""

    args: List[str] = request.args.getlist('arg')
    clean_args: List[str] = [shlex.quote(arg) for arg in args]
    command = ['ps'] + clean_args
    result = run(command, stdout=PIPE, stderr=PIPE, encoding='utf-8')
    output = result.stdout.strip()
    return f"<pre>{output}</pre>"


if __name__ == '__main__':
    app.run(debug=True)
