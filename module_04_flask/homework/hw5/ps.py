from flask import Flask, request
from subprocess import run
from typing import List
import shlex

app = Flask(__name__)


@app.route('/ps', methods=['GET'])
def execute_ps() -> str:
    """The function returns result of performing 'ps' command."""

    args_list: List[str] = request.args.getlist('arg')
    args_string: str = shlex.quote("".join(args_list))
    command_str = f"ps {args_string}"
    command = shlex.split(command_str)
    result = run(command, capture_output=True)
    return f"<pre>{result}</pre>"


if __name__ == '__main__':
    app.run(debug=True)




# from flask import Flask, request
# from subprocess import run, PIPE
# from typing import List
# import shlex
#
# app = Flask(__name__)
#
#
# @app.route('/ps', methods=['GET'])
# def execute_ps() -> str:
#     args: List[str] = request.args.getlist('arg')
#     command = ['ps'] + args
#     result = run(command, stdout=PIPE, stderr=PIPE, encoding='utf-8')
#     output = result.stdout.strip()
#     return f"<pre>{output}</pre>"
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
