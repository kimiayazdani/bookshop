import json

from flask import Flask, render_template, request, url_for, jsonify


from http import HTTPStatus



app = Flask(__name__)
path = "http://127.0.0.1:"
port_nums = {'admin':8001, 'client':8002, 'search':8003, 'book':8004}




if __name__ == '__main__':
    app.run(debug=True, port=8004)

