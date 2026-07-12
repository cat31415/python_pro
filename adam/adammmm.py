from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

users = [
    {"id": 1, "name": "Alice", "birth_date": "1995-05-15"},
    {"id": 2, "name": "Bob", "birth_date": "1992-10-20"},
    {"id": 3, "name": "Charlie", "birth_date": "1988-03-01"},
    {"id": 4, "name": "Alice", "birth_date": "2000-12-25"},
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

@app.get("/users/name/{user_name}")
def get_users_by_name(user_name: str):
    matched_users = [user for user in users if user["name"].lower() == user_name.lower()]
    return {"users": matched_users}

@app.get("/cat")
def get_cat():
    return {"message": "Meow!"}

@app.post("/users/set_name/{user_id}",
          description="Update the name of a user by their ID",
          summary="Update user name")
def set_name(user_id: int, name: str = Query(description="New name for the user", example="Alice")):
    for user in users:
        if user["id"] == user_id:
            user["name"] = name
            return {"message": f"User {user_id} name updated to {name}"}
    return {"error": "User not found"}

@app.post("/users/set_birth_date/{user_id}")
def set_birth_date(user_id: int, birth_date: str = Query(description="New birth date (YYYY-MM-DD)", example="1995-05-15")):
    for user in users:
        if user["id"] == user_id:
            user["birth_date"] = birth_date
            return {"message": f"User {user_id} birth date updated to {birth_date}"}
    return {"error": "User not found"}

@app.get("/users/get_birth_date/{user_id}")
def get_birth_date(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return {"birth_date": user.get("birth_date")}
    return {"error": "User not found"}
