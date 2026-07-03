from pydantic import BaseModel
from typing import Literal 

class Room(BaseModel):
    id: int
    name: str
    size: Literal["S", "M", "L"]
    is_vip: bool = False



