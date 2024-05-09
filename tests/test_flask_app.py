import json
import sys

import requests

sys.path.append("../project2/")

from data import goals, teachers

host = "www.example.com"


def make_a_request(method, url, headers={"host": host}, **kwargs):
    return requests.request(method, url, headers=headers, **kwargs)


def test_teacher_page():
    url = "http://127.0.0.1:8000/profiles/4/"
    r = make_a_request("get", url)
    assert r.status_code == 200
    assert "Gulya S" in r.text
    assert "/booking/4/wed/16:00/" in r.text
    print("Test #1 passed.")


def test_404_error():
    url = "http://127.0.0.1:8000/4/"
    r = make_a_request("get", url)
    assert r.status_code == 404
    print("Test #2 passed.")


def test_booking():
    url = "http://127.0.0.1:8000/booking_done/"
    payload = {
        "clientName": "Nikita",
        "clientPhone": "8-999-999-99-99",
        "clientTime": "10:00",
        "clientTeacher": "0",
        "clientWeekday": "mon",
    }
    r = make_a_request("post", url, data=payload)
    assert r.status_code == 200
    assert "<p><b>Тема:</b> Пробный урок</p>" in r.text
    assert "<p><b>Дата:</b> Понедельник, 10:00</p>" in r.text
    assert "<p><b>Имя:</b> Nikita</p>" in r.text
    assert "<p><b>Телефон:</b> 8-999-999-99-99</p>" in r.text
    with open(r"../project2/booking.json", "r") as database:
        database_content = json.loads(database.read())
        assert database_content[-1]["name"] == "Nikita"
        assert database_content[-1]["phone"] == "8-999-999-99-99"
    print("Test #3 passed.")


def test_request():
    url = "http://127.0.0.1:8000/request_done/"
    payload = {
        "clientName": "Senior Pomidor",
        "clientPhone": "8-800-555-35-35",
        "goal": "work",
        "time": "7-10",
    }
    r = make_a_request("post", url, data=payload)
    assert r.status_code == 200
    assert "<p><b>Цель занятий:</b> Для работы</p>" in r.text
    assert "<p><b>Времени есть:</b> 7-10" in r.text
    assert "<p><b>Имя:</b> Senior Pomidor</p>" in r.text
    assert "<p><b>Телефон:</b> 8-800-555-35-35</p>" in r.text
    with open(r"../project2/request.json", "r") as database:
        database_content = json.loads(database.read())
        assert database_content[-1]["name"] == "Senior Pomidor"
        assert database_content[-1]["phone"] == "8-800-555-35-35"
    print("Test #4 passed.")


def test_goal_page():
    url = "http://127.0.0.1:8000/goals/{}/"
    for goal in goals:
        r = make_a_request("get", url.format(goal))
        assert r.status_code == 200
        assert goal in r.url
        assert f"<br>Преподаватели <br> {goals[goal].lower()}" in r.text
        assert r.text.count('<div class="card mb-4">') > 2
    else:
        print("Test #5 passed.")


def test_main_page():
    url = "http://127.0.0.1:8000/"
    r = make_a_request("get", url)
    assert r.status_code == 200
    assert (
        '<a href="goals/travel/" class="btn btn-outline-secondary">⛱ Для путешествий</a>'
        in r.text
    )
    assert (
        '<a href="goals/study/" class="btn btn-outline-secondary">🏢 Для учебы</a>'
        in r.text
    )
    assert (
        '<a href="goals/work/" class="btn btn-outline-secondary">🏫 Для работы</a>'
        in r.text
    )
    assert (
        '<a href="goals/relocate/" class="btn btn-outline-secondary">🚜 Для переезда</a>'
        in r.text
    )
    assert (
        '<a href="/request/" class="btn btn-primary">Заказать подбор</a>'
        in r.text
    )
    assert r.text.count('<div class="card mb-4">') == 6
    print("Test #6 passed.")


def test_all_teachers_page():
    url = "http://127.0.0.1:8000/all/"
    r = make_a_request("get", url)
    assert r.status_code == 200
    assert r.text.count('<div class="card mb-4">') == len(teachers) + 1
    # <div class="card mb-4"> - Карточка преподавателя, преподавателей 12,
    # но эта карточка также используется для размещения фильтров, поэтому
    # всего 13.
    assert (
        '<p class="lead float-left d-inline-block mt-2 mb-0"><strong>12 преподавателей в\n              базе</strong></p>'
        in r.text
    )
    payload = {"filter": "4"}
    r = make_a_request("post", url, data=payload)
    assert r.status_code == 200
    assert r.text.count('<div class="card mb-4">') == len(teachers) + 1
    payload = {"filter": "3"}
    r = make_a_request("post", url, data=payload)
    assert r.status_code == 200
    assert r.text.count('<div class="card mb-4">') == len(teachers) + 1
    best_rating = """<button type="submit" class="btn btn-primary my-1">Сортировать</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    
    <div class="card mb-4">
      <div class="card-body">
        <div class="row">
          <div class="col-3"><img src="https://i.pravatar.cc/300?img=35" class="img-fluid" alt="Skye L."></div>
          <div class="col-9">
            <p class="float-right">Рейтинг: 5 Ставка: 1700 / час</p>
            <h2 class="h4">Skye L.</h2>
            <p>Hello, My name is Skye. I’m from London in the United Kingdom but I am currently living in Japan. I have a TEFL certificate which I acquired last year. Since moving to Japan I have been teaching some of my Japanese friends English. I think learning should be fun and engaging and even though English can be difficult to learn I aim to make it enjoyable.I enjoy watching football and travelling. I do a lot of Yoga in my spare time and I can&#39;t wait to meet you!</p>
            <a href="profiles/8/" class="btn btn-outline-primary btn-sm mr-3 mb-2">Показать информаци и
              расписание</a>
          </div>
        </div>
      </div>
    </div>
    """
    assert best_rating in r.text
    payload = {"filter": "1"}
    r = make_a_request("post", url, data=payload)
    most_expensive = """<button type="submit" class="btn btn-primary my-1">Сортировать</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    
    <div class="card mb-4">
      <div class="card-body">
        <div class="row">
          <div class="col-3"><img src="https://i.pravatar.cc/300?img=35" class="img-fluid" alt="Skye L."></div>
          <div class="col-9">
            <p class="float-right">Рейтинг: 5 Ставка: 1700 / час</p>
            <h2 class="h4">Skye L.</h2>
            <p>Hello, My name is Skye. I’m from London in the United Kingdom but I am currently living in Japan. I have a TEFL certificate which I acquired last year. Since moving to Japan I have been teaching some of my Japanese friends English. I think learning should be fun and engaging and even though English can be difficult to learn I aim to make it enjoyable.I enjoy watching football and travelling. I do a lot of Yoga in my spare time and I can&#39;t wait to meet you!</p>
            <a href="profiles/8/" class="btn btn-outline-primary btn-sm mr-3 mb-2">Показать информаци и
              расписание</a>
          </div>
        </div>
      </div>
    </div>"""
    assert most_expensive in r.text
    payload = {"filter": "2"}
    r = make_a_request("post", url, data=payload)
    cheapest = """<button type="submit" class="btn btn-primary my-1">Сортировать</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    
    <div class="card mb-4">
      <div class="card-body">
        <div class="row">
          <div class="col-3"><img src="https://i.pravatar.cc/300?img=30" class="img-fluid" alt="Yan M"></div>
          <div class="col-9">
            <p class="float-right">Рейтинг: 3.9 Ставка: 800 / час</p>
            <h2 class="h4">Yan M</h2>
            <p>Hello! My name is Yang and for more than five years I have been teaching English. I spent part of this time in China, where I worked with students from 3 to 40 years old. I deal with both adults and children. But for all ages, I try to make my classes fun and interactive. Teaching English to me is not just a language lesson. I always try to attract a wider cultural and historical context that helps my students understand more about the language and its features. A degree in history helps me a lot to create such an intellectual environment in the classroom.For each student, I develop an individual curriculum that depends on its goals and needs.</p>
            <a href="profiles/5/" class="btn btn-outline-primary btn-sm mr-3 mb-2">Показать информаци и
              расписание</a>
          </div>
        </div>
      </div>
    </div>"""
    assert cheapest in r.text
    print("Test #7 passed.")
