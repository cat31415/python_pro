'''
HTTP - HyperText Transfer Protocol - протокол(набор правил) передачи данных в интернете.
 Он определяет, как сообщения форматируются и передаются, а также какие действия должны предпринимать 
 веб-серверы и браузеры в ответ на различные команды.

app1 -> app2 -> app3

hhtp запрос состаит из заголовка и тела запроса. Заголовок содержит метаинформацию о запросе,
 такую как тип данных, язык, авторизацию и т.д. Тело запроса содержит данные, которые отправляются на сервер,

 Типы HTTP запросов:
    - GET: используется для получения данных с сервера. Запросы GET не должны изменять состояние сервера.
    - POST: используется для отправки данных на сервер. Запросы POST могут изменять состояние сервера, например, создавать новые ресурсы или обновлять существующие.
    - PUT: используется для обновления существующих ресурсов на сервере. Запросы PUT могут изменять состояние сервера.
    - DELETE: используется для удаления ресурсов на сервере. Запросы DELETE могут изменять состояние сервера.

установить FastAPI и Uvicorn для создания веб-приложения на Python:
pip install fastapi uvicorn

запустить приложение:
uvicorn lesson:app --reload (--port 8002 не обязательно, по умолчанию используется порт 8000)
'''

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
    {"id": 4, "name": "Alice"},
]

@app.get("/")
def home():
    return {"message": "Hello, World!"}

@app.get("/users")
def get_users():
    return {"users": users}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return {"user": user}
    return {"error": "User not found"}

#создать ручку /users/name/{user_name}, которая будет возвращать пользователей с именем, совпадающим с user_name

@app.get("/cat")
def get_cat():
    return {"message": "Meow!"}