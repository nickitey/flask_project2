import json
from datetime import datetime

from flask import Flask, render_template, request

from create_db import create_json_db
from tools import get_list_of_random_ids, update_json_database

# Создаем нашу json-database из мок-данных в data.py
create_json_db()

# Читаем нашу json-database и получаем из нее данные
with open(r"database.json", "r") as db:
    content = json.load(db)

# Распакуем на две независимые части
target, teachers, emojis = content

week = {
    "mon": "Понедельник",
    "tue": "Вторник",
    "wed": "Среда",
    "thu": "Четверг",
    "fri": "Пятница",
    "sat": "Суббота",
    "sun": "Воскресенье",
}

app = Flask(__name__)
app.secret_key = "abcdefu"


@app.route("/")
def render_main():
    teacher_ids = get_list_of_random_ids(6, teachers)
    return render_template(
        "index.html",
        teacher_ids=teacher_ids,
        teachers=teachers,
        goals_emoji=emojis,
        goals=target,
    )


@app.route("/all/", methods=["GET", "POST"])
def render_teachers():
    if request.method == "GET":
        teachers_id = get_list_of_random_ids(len(teachers), teachers)
        selected_value = "4"
        return render_template(
            "all.html",
            teachers=teachers,
            teachers_id=teachers_id,
            selected_value=selected_value,
        )
    else:
        select_value = request.form["filter"]
        if select_value == "4":
            teachers_id = get_list_of_random_ids(len(teachers), teachers)
            sort_filter = None
            reverse_status = None
        elif select_value == "3":
            teachers_id = None
            sort_filter = "rating"
            reverse_status = True
        elif select_value == "2":
            teachers_id = None
            sort_filter = "price"
            reverse_status = False
        else:
            teachers_id = None
            sort_filter = "price"
            reverse_status = True
        return render_template(
            "all.html",
            teachers=teachers,
            teachers_id=teachers_id,
            sort_filter=sort_filter,
            reverse_status=reverse_status,
            select_value=select_value,
        )


@app.route("/goals/<goal>/")
def render_goal(goal):
    return render_template(
        "goal.html",
        target=target,
        goal=goal,
        teachers=teachers,
        goals_emoji=emojis,
    )


@app.route("/profiles/<teacher_id>/")
def render_teacher(teacher_id):
    try:
        teacher = teachers[int(teacher_id)]
        return render_template(
            "profile.html", teacher=teacher, week=week, goals=target
        )
    except IndexError:
        return render_template("404.html")


@app.route("/request/")
def render_request():
    enumerated_goals = list(enumerate(target, 1))
    return render_template(
        "request.html", enumerated=enumerated_goals, target=target
    )


@app.route("/request_done/", methods=["POST"])
def render_request_done():
    client_name = request.form["clientName"]
    client_phone = request.form["clientPhone"]
    time = request.form["time"]
    goal = request.form["goal"]
    goal_to_template = target[goal]
    teacher_request = [
        {
            "request_id": None,
            "name": client_name,
            "phone": client_phone,
            "goal": goal,
            "time": time,
            "order_date": datetime.now().strftime("%d-%m-%Y"),
            "order_time": datetime.now().strftime("%H:%M:%S"),
        }
    ]
    update_json_database(
        "request.json", teacher_request, order_key="request_id"
    )
    return render_template(
        "request_done.html",
        clientName=client_name,
        clientPhone=client_phone,
        time=time,
        goal=goal_to_template,
    )


@app.route("/booking/<teacher_id>/<dow>/<time>/")
def render_booking(teacher_id, dow, time):
    teacher = teachers[int(teacher_id)]
    return render_template(
        "booking.html", teacher=teacher, week=week, time=time, dow=dow
    )


@app.route("/booking_done/", methods=["POST"])
def render_booking_done():
    client_name = request.form["clientName"]
    client_day = request.form["clientWeekday"]
    client_time = request.form["clientTime"]
    client_phone = request.form["clientPhone"]
    client_teacher = request.form["clientTeacher"]
    order = [
        {
            "orderID": None,
            "name": client_name,
            "day": client_day,
            "client_time": client_time,
            "phone": client_phone,
            "teacherID": client_teacher,
            "order_date": datetime.now().strftime("%d-%m-%Y"),
            "order_time": datetime.now().strftime("%H:%M:%S"),
        }
    ]
    update_json_database("booking.json", order, order_key="orderID")
    return render_template(
        "booking_done.html",
        week=week,
        clientName=client_name,
        clientTime=client_time,
        clientPhone=client_phone,
        clientDay=client_day,
    )


@app.errorhandler(500)
def render_server_error(error):
    return "Что-то не так, но мы все починим, честное слово.", 500


@app.errorhandler(404)
def render_404_error(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run()
