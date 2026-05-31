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

@app.get("/cat")
def cat():
    return {"message": "Meow!"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return {"user": user}
    return {"error": "User not found"}

@app.get("/users/name/{user_name}")
def get_user(user_name: str): 
    for user2 in users:
        if user2["name"] == user_name:
            return {"user": user2}
    return {"error": "usres not found"}    
 