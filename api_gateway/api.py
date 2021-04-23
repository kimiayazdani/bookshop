import json

from flask import Flask, render_template, request, url_for, jsonify
import requests

from http import HTTPStatus

app = Flask(__name__)
path = "http://127.0.0.1:"
port_nums = {'admin': '8001', 'client': '8002', 'search': '8003', 'book': '8004'}

#ACCOUNTS FUNCTION

@app.route('/client/login/', methods=['POST'])
def login_client():
    return requests.post(path + port_nums['client'] + '/api/account/login/', json=request.json)


@app.route('/admin/login/', methods=['POST'])
def login_admin():
    return requests.post(path + port_nums['admin'] + '/api/account/login/', json=request.json)


@app.route('/client/show/', methods=['GET'])
def show_profile_client():
    # no need for ID since token is handled.
    return requests.get(path + port_nums['client'] + '/api/account/properties/', headers=request.headers)


@app.route('/admin/show/', methods=['GET'])
def show_profile_admin():
    # no need for ID since token is handled.
    return requests.get(path + port_nums['admin'] + '/api/account/properties/', headers=request.headers)


@app.route('/client/register/', methods=['POST'])
def register_client():
    return requests.post(path + port_nums['client'] + '/api/account/register/', json=request.json)


@app.route('/admin/update/', methods=['PATCH'])
def update_admin():
    return requests.patch(path + port_nums['admin'] + '/api/account/update/', json=request.json)


@app.route('/client/update/', methods=['PATCH'])
def update_client():
    return requests.patch(path + port_nums['client'] + '/api/account/update/', json=request.json)


@app.route('/client/refreshtoken/', methods=['POST'])
def refresh_token_client():
    return requests.post(path + port_nums['client'] + '/api/token/refresh/', json=request.json)

@app.route('/admin/refreshtoken/', methods=['POST'])
def refresh_token_admin():
    return requests.post(path + port_nums['admin'] + '/api/token/refresh/', json=request.json)

#BOOK FUNCTION
@app.route('/book/read/<int:id>', methods=['POST'])
def book_read(id):
    res = requests.get(path + port_nums['admin'] + '/api/account/properties/', headers=request.headers)    
    if res.status_code > 199 and res.status_code < 300:
        return requests.get(path + port_nums['admin'] + '/api/v1/book/post/'+str(id)+"/")
    return res


if __name__ == '__main__':
    app.run(debug=True, port=8000)
