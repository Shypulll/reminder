import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')
# 🔹 URL запроса
URL = "https://mojeaeh.vizja.pl/vizja-stud-app/ledge/view/AJAX"

# 🔹 Заголовки (из твоего браузера)
HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru,en;q=0.9,pl;q=0.8",
    "Connection": "keep-alive",
    "Content-Length": "134",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "mojeaeh.vizja.pl",
    "Origin": "https://mojeaeh.vizja.pl",
    "Referer": "https://mojeaeh.vizja.pl/vizja-stud-app/ledge/view/stud.schedule.SchedulePage",
    "Sec-Ch-Ua": '"Chromium";v="130", "YaBrowser";v="24.12", "Not?A_Brand";v="99", "Yowser";v="2.5"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 YaBrowser/24.12.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    # ❗ Вставь свои Cookies!
    "Cookie": "JSESSIONID=D7A42A0355817FC01A142415DAF0799C; _ga=GA1.1.1908296875.1738014261"
}

# 🔹 Данные для запроса (из "Payload")
DATA = {
    "service": "Planowanie",
    "method": "getUlozoneTerminyOsoby",
    "params": {
        "idOsoby": 62243,  # Твой ID студента
        "idSemestru": 89,  # ID семестра
        "poczatekTygodnia": 1742770800000  # Начало недели
    }
}

# 🔹 Отправляем запрос
response = requests.post(URL, headers=HEADERS, data=json.dumps(DATA))

# 🔹 Проверяем ответ
if response.status_code == 200:
    print("Успешно получили расписание!")
    print("Данные:", response.json())  # Выводим JSON с расписанием
else:
    print("Ошибка! Код:", response.status_code)
    print("Ответ сервера:", response.text)
