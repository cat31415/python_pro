from pydantic import BaseModel

from datetime import datetime

class Booking(BaseModel):
    room_id: int
    user_name: str
    start_time: datetime
    end_time: datetime
