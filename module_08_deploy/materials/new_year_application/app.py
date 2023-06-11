import os

from flask import Flask, render_template, send_from_directory

root_dir = os.path.dirname(os.path.abspath(__file__))

template_folder = os.path.join(root_dir, "templates")
static_folder = os.path.join(root_dir, "static")
js_directory = os.path.join(static_folder, "js")
css_directory = os.path.join(static_folder, "css")
images_directory = os.path.join(static_folder, "images")

app = Flask(__name__, template_folder=template_folder)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/static/<string:folder>/<path:path>")
def send_static(folder, path):
    if folder == "js":
        return send_from_directory(js_directory, path)
    elif folder == "css":
        return send_from_directory(css_directory, path)
    elif folder == "images":
        return send_from_directory(images_directory, path)


if __name__ == "__main__":
    app.run()
