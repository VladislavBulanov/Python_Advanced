from flask import Flask, make_response
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    resp = make_response("{'123':'aaa'}")
    return resp


if __name__ == '__main__':
    #WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run()
