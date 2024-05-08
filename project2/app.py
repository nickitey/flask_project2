import json
from datetime import datetime
import random

from create_db import create_json_db
from flask import Flask, render_template, request
from tools import update_json_database


# Создаем нашу json-database из мок-данных в data.py
create_json_db()

# Читаем нашу json-database и получаем из нее данные
with open(r"database.json", "r") as db:
    content = json.load(db)

# Распакуем на две независимые части
target, teachers = content

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
    teacher_ids = set()
    while len(teacher_ids) < 6:
        teacher_ids.add(random.randint(0, len(teachers) - 1))
    return render_template("index.html", teacher_ids=teacher_ids,
                           teachers=teachers)


@app.route("/all")
def render_teachers():
    return "3десь будут преподаватели"


@app.route("/goals/<goal>")
def render_goal(goal):
    return render_template('goal.html', target=target, goal=goal,
                           teachers=teachers)


@app.route("/profiles/<teacher_id>")
def render_teacher(teacher_id):
    try:
        teacher = teachers[int(teacher_id)]
        return render_template("profile.html", teacher=teacher, week=week)
    except IndexError:
        return render_template("404.html")


@app.route("/request")
def render_request():
    return render_template("request.html")


@app.route("/request_done", methods=["POST"])
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
    update_json_database("request.json", teacher_request, order_key="request_id")
    return render_template(
        "request_done.html",
        clientName=client_name,
        clientPhone=client_phone,
        time=time,
        goal=goal_to_template,
    )


@app.route("/booking/<teacher_id>/<dow>/<time>")
def render_booking(teacher_id, dow, time):
    teacher = teachers[int(teacher_id)]
    return render_template(
        "booking.html", teacher=teacher, week=week, time=time, dow=dow
    )


@app.route("/booking_done", methods=["POST"])
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
    return f"Что-то не так, но мы все починим, честное слово.", 505


@app.errorhandler(404)
def render_404_error(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run()
