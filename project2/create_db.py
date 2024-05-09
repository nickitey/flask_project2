import json

from data import goals, teachers, goals_emoji


def create_json_db():
    to_json = [goals, teachers, goals_emoji]
    json_string = json.dumps(to_json, indent=4)
    with open(r"database.json", "w") as database:
        database.write(json_string)
