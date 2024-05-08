import json

from data import goals, teachers

to_json = [goals, teachers]
json_string = json.dumps(to_json, indent=4)
with open(r"database.json", "w") as database:
    database.write(json_string)
