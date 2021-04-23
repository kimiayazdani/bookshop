import json


def sort_by_title_and_category(json_data, title=None, category=None):
    data = json.load(json_data)
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

    return output


file = open("../books.json", 'r')
print(sort_by_title_and_category(file, title="Design Pattern"))