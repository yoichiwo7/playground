from flask import Flask, render_template, url_for, send_from_directory, request
import os

app = Flask(__name__, static_url_path='')

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

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


if __name__ == "__main__":
    app.run(debug=True)
