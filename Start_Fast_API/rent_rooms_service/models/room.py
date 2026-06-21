from pydantic import BaseModel

class Room(BaseModel):
    id: int
    name: str
    size: str
    is_vip: bool = False



