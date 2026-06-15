from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
# 2:app --reload
robots = [
    "Explorer-1",
    "Builder-2",
    "Miner-3"
]

@app.get("/robots")
def get_rob():
    return {"rob": robots}


@app.get("/robots/{rob_id}")
def get_rob_id(rob_id: int):
    robotss = robots[rob_id]
    return {"rob": robotss}
        
