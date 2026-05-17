from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, World!"}

@app.get("/cat")
def cat():
    return {"message": "Meow!"}
