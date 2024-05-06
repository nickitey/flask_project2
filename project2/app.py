import json

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
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
    return f"3десь будет форма бронирования учителя {teacher_id} " f"на {dow} в {time}"


@app.route("/booking_done")
def render_booking_done():
    return "3аявка отправлена"


@app.errorhandler(500)
def render_server_error(error):
    return f"Что-то не так, но мы все починим, честное слово.", error


@app.errorhandler(404)
def render_404_error(error):
    return render_template("404.html")


if __name__ == "__main__":
    app.run()
