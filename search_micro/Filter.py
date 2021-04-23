import json

from flask import Flask, render_template, request, url_for, jsonify


from http import HTTPStatus



app = Flask(__name__)


@app.route('/book/search/', methods=['POST'])
def sort_by_title_and_category(json_data):
    data = json.load(json_data)
    title = data['title']
    category = data['category']
    if category is not None:
        sort_by_category = {"books": []}
        for book in data["books"]:
            if category in book["category"]:
                sort_by_category["books"].append(book)
    else:
        sort_by_category = data
    output = {"books": []}
    if title is not None:

        for book in sort_by_category["books"]:
            if title in book["title"]:
                output["books"].append(book)
    else:
        output = sort_by_category

    return jsonify(output), HTTPStatus.OK

if __name__ == '__main__':
    app.run(debug=True, port=8004)

