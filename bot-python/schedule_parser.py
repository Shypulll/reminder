import requests
import json
from datetime import datetime


def format_time(timestamp):
    return datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M')


def get_schedule():
    URL = "https://mojeaeh.vizja.pl/vizja-stud-app/ledge/view/AJAX"

    HEADERS = {
        "Content-Type": "application/json",
        "Cookie": "JSESSIONID=D7A42A0355817FC01A142415DAF0799C"  # ❗ Вставь свои Cookie
    }

    DATA = {
        "service": "Planowanie",
        "method": "getUlozoneTerminyOsoby",
        "params": {
            "idOsoby": 62243,
            "idSemestru": 89,
            "poczatekTygodnia": 1742770800000
        }
    }

    response = requests.post(URL, headers=HEADERS, data=json.dumps(DATA))

    if response.status_code == 200:
        data = response.json().get('returnedValue', {}).get('items', [])
        schedule = []

        for lesson in data:
            schedule.append({
                "subject": lesson.get('nazwaPelnaPrzedmiotu', 'Без названия'),
                "start_time": format_time(lesson['dataRozpoczecia']),
                "end_time": format_time(lesson['dataZakonczenia']),
                "teacher": lesson.get('wykladowcy', [{}])[0].get('stopienImieNazwisko', 'Преподаватель не указан'),
                "location": lesson.get('sale', [{}])[0].get('nazwaSkrocona', 'Аудитория не указана')
            })

        return schedule
    else:
        return []
