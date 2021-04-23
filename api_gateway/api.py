import json

from flask import Flask, render_template, request, url_for, jsonify
import requests

from http import HTTPStatus



app = Flask(__name__)
path = "http://127.0.0.1:"
port_nums = {'admin':8001, 'client':8002, 'search':8003, 'book':8004}


@app.route('/client/login/', methods=['POST'])
def login_client():
    return requests.post(path+client+'/api/account/login/', json=request.json)

@app.route('/admin/login/', methods=['POST'])
def login_admin():
    return requests.post(path+admin+'/api/account/login/', json=request.json)


if __name__ == '__main__':
    app.run(debug=True, port=8000)

