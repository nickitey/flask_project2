from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField

app = Flask(__name__)
app.secret_key = "abcdefu"


@app.route("/")
def render_main():
    return "3десь будет главная"


@app.route("/all")
def render_teachers():
    return "3десь будут преподаватели"


@app.route("/goals/<goal>")
def render_goal(goal):
    return f"3десь будет цель {goal}"


@app.route("/profiles/<teacher_id>")
def render_teacher(teacher):
    return f"3десь будет преподаватель {teacher}"


@app.route("/request")
def render_request():
    return "3десь будет заявка на подбор"


@app.route("/request_done/")
def render_request_done():
    return "3аявка на подбор отправлена"


@app.route("/booking/<teacher_id>/<dow>/<time>")
def render_booking(teacher_id):
    return f"3десь будет форма бронирования {teacher_id}"


@app.route("/booking_done")
def render_booking_done():
    return "3аявка отправлена"


if __name__ == "__main__":
    app.run()
