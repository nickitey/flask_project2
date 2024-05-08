import json

from project2.data import goals, teachers


def create_json_db():
    to_json = [goals, teachers]
    json_string = json.dumps(to_json, indent=4)
    with open(r"database.json", "w") as database:
        database.write(json_string)
