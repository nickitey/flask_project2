import json
import random


def update_json_database(database_name, data_to_fill, need_number=True, order_key=None):
    try:
        database_start = open(database_name, "r")
        try:
            database_content = json.loads(database_start.read())
        except json.decoder.JSONDecodeError:
            database_content = []
        database_full = database_content + data_to_fill
        database_start.close()
        if need_number:
            database_full = update_order_number(database_full, order_key)
        database_finish = open(database_name, "w")
        database_finish.write(json.dumps(database_full))
        database_finish.close()
    except IOError:
        database_new = open(database_name, "w")
        database_new.write(json.dumps(update_order_number(data_to_fill, order_key)))
        database_new.close()
    print(f"{database_name} is updated.")


def update_order_number(data, key):
    if len(data) > 0:
        data[-1][key] = len(data)
    else:
        data[0][key] = 1
    return data


def get_list_of_random_ids(target_length, max_length_obj):
    unique_ids = set()
    target_ids = list()
    while len(target_ids) < target_length:
        new_id = random.randint(0, len(max_length_obj) - 1)
        if new_id not in unique_ids:
            target_ids.append(new_id)
            unique_ids.add(new_id)
    return target_ids
