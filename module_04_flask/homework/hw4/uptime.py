from flask import Flask
from subprocess import check_output

app = Flask(__name__)


@app.route('/uptime', methods=['GET'])
def get_uptime():
    uptime = check_output(['uptime', '-p']).decode().strip()[3:]
    return f"Current uptime is {uptime}"


if __name__ == '__main__':
    app.run(debug=True)
