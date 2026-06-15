from fastapi import FastAPI
from pydantic import BaseModel
# uvicorn main:app --reload
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

@app.get("/users/{user_id}",
        description="получить пользователя по id",
        summary="получить по id"
         )
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return {"user": user}
    return {"error": "User not found"}

@app.get("/users/name/{user_name}",
         description="получить пользователя по имени",
         summary="получить пользвателя"
        )
def get_user(user_name: str): 
    for user2 in users:
        if user2["name"] == user_name:
            return {"user": user2}
    return {"error": "usres not found"}  

  

@app.post("/users/set_name/{user_id}",
          description="Update the name of a user by their ID",
          summary="Update user name")
def set_name(user_id: int, name: str = Query(description="New name for the user", example="Alice")):
    for user in users:
        if user["id"] == user_id:
            user["name"] = name
            return {"message": f"User {user_id} name updated to {name}"}
    # выводим ошибку, если пользователь не найден
    return {"error": "User not found"}


@app.post("/users/set_birth_date/{user_id}",
          description="",
          summary=""
          ) 
def set_data(user_id: int, data: str = Query(description="", example="")):
    for usr in users:
        if usr["id"] == user_id:
            usr["data"] = data
            return{"message": f"User {user_id} updated to data {data}"}
    return {"error": "User not found"}

  
#  добавить пользователям дату рождения: str в формате "YYYY-MM-DD" и 
# создать ручку /users/set_birth_date/{user_id}, которая будет обновлять дату
#  рождения пользователя по id, а также ручку /users/get_birth_date/{user_id}, 
# которая будет возвращать дату рождения пользователя по id.