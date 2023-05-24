import subprocess
from flask import Flask, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange

app = Flask(__name__)


class CodeForm(FlaskForm):
    """The FlaskForm class."""

    code = StringField('Code', validators=[
        InputRequired("The field 'code' is required")
    ])
    timeout = IntegerField('Timeout', validators=[
        InputRequired("The field 'timeout' is required"),
        NumberRange(min=1, max=30)
    ])


def run_python_code_in_subprocess(code: str, timeout: int):
    """
    The function takes Python code and timeout
    and returns a result of performing of this program.
    If execution time is more than timeout process is terminated
    and user gets error message.
    :param code: the Python code
    :param timeout: timeout in seconds
    """

    command = ['python3', '-c', f'{code}']
    # command = [
    #     'prlimit', f'--cpu={timeout}', '--nproc=1:1', 'python3', '-c', code
    # ]
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False
    )

    try:
        stdout, stderr = process.communicate(timeout=timeout)
        result = stdout.decode('utf-8')

    except subprocess.TimeoutExpired:
        process.terminate()
        process.wait(timeout=1)
        result = 'Execution time exceeded the timeout limit.'

    return result


@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm(request.form)
    if form.validate_on_submit():
        code = form.code.data
        timeout = form.timeout.data
        result = run_python_code_in_subprocess(code, timeout)
        return result

    return f"Invalid input, {form.errors}", 400


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
