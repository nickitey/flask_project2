import json

import requests

host = "www.example.com"


def test_teacher_page():
    url = "http://127.0.0.1:8000/profiles/4"
    r = requests.get(url, headers={"host": host})
    assert r.status_code == 200
    assert "Gulya S" in r.text
    assert "/booking/4/wed/16:00" in r.text
    print("Test #1 passed.")


def test_404_error():
    url = "http://127.0.0.1:8000/4"
    r = requests.get(url, headers={"host": host})
    assert r.status_code == 404
    print("Test #2 passed.")


def test_booking():
    url = "http://127.0.0.1:8000/booking_done"
    payload = {
        "clientName": "Nikita",
        "clientPhone": "8-999-999-99-99",
        "clientTime": "10:00",
        "clientTeacher": "0",
        "clientWeekday": "mon",
    }
    r = requests.post(url, data=payload)
    assert r.status_code == 200
    assert "<p><b>Тема:</b> Пробный урок</p>" in r.text
    assert "<p><b>Дата:</b> Понедельник, 10:00</p>" in r.text
    assert "<p><b>Имя:</b> Nikita</p>" in r.text
    assert "<p><b>Телефон:</b> 8-999-999-99-99</p>" in r.text
    with open(r'../project2/booking.json', 'r') as database:
        database_content = json.loads(database.read())
        assert database_content[-1]['name'] == 'Nikita'
        assert database_content[-1]['phone'] == '8-999-999-99-99'
    print("Test #3 passed.")


def test_request():
    url = "http://127.0.0.1:8000/request_done"
    payload = {
        'clientName': 'Senior Pomidor',
        'clientPhone': '8-800-555-35-35',
        'goal': 'work',
        'time': '7-10'
    }
    r = requests.post(url, data=payload)
    assert r.status_code == 200
    assert '<p><b>Цель занятий:</b> Для работы</p>' in r.text
    assert '<p><b>Времени есть:</b> 7-10' in r.text
    assert '<p><b>Имя:</b> Senior Pomidor</p>' in r.text
    assert '<p><b>Телефон:</b> 8-800-555-35-35</p>' in r.text
    with open(r'../project2/request.json', 'r') as database:
        database_content = json.loads(database.read())
        assert database_content[-1]['name'] == 'Senior Pomidor'
        assert database_content[-1]['phone'] == '8-800-555-35-35'
    print('Test # 4 passed.')


def test_goal_page():
    url = "http://127.0.0.1:8000/goals/"
