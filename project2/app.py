import json

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from tools import update_json_database, update_order_number
from wtforms import BooleanField, PasswordField, SelectField, StringField

with open(r"database.json", "r") as db:
    content = json.load(db)

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
    return render_template("index.html")


@app.route("/all")
def render_teachers():
    return "3десь будут преподаватели"


@app.route("/goals/<goal>")
def render_goal(goal):
    return f"3десь будет цель {goal}"


@app.route("/profiles/<teacher_id>")
def render_teacher(teacher_id):
    try:
        teacher = teachers[int(teacher_id)]
        return render_template("profile.html", teacher=teacher, week=week)
    except IndexError:
        return render_template("404.html")


@app.route("/request")
def render_request():
    return "3десь будет заявка на подбор"


@app.route("/request_done/")
def render_request_done():
    return "3аявка на подбор отправлена"


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
            "time": client_time,
            "phone": client_phone,
            "teacherID": client_teacher,
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
