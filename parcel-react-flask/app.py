from flask import Flask, render_template, url_for, send_from_directory, request
import os

app = Flask(__name__, static_url_path='')

@app.route("/")
def sap():
    print(os.getcwd())
    return send_from_directory("static", "index.html")

@app.route("/hello")
def hello():
    return "hello world. 日本語にも対応"

@app.route("/echo", methods=['POST'])
def echo():
    return request.data


@app.route("/<int:bars_count>/")
def chart(bars_count):
    if bars_count <= 0:
        bars_count = 1
    return render_template("chart.html", bars_count=bars_count)


if __name__ == "__main__":
    app.run(debug=True)
