from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
# mai:app --reload
robots = [
    {"id": 0, "name": "Explorer-1"},
    {"id": 1, "name": "Builder-2"},
    {"id": 2, "name": "Miner-3"}
]

@app.get("/robots",
    description="получить всех роботов",    
)
def get_rob():
    return {"rob": robots}


@app.get("/robots/{rob_id}")
def get_rob_id(rob_id: int):
    for rob in robots:
        if rob["id"] == rob_id: 
            return {"rob": rob}
        
@app.post("/robots")
def new_rob(name: str):
    id = []
    for r in robots:
        id.append(r["id"])
        
    max_id = max(id)
    new_id = max_id + 1
    robots.append({"id": new_id, "name": name})
    return 


        
