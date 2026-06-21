from pydantic import BaseModel

from datetime import datetime

class Booking(BaseModel):
    room_id: id
    user_name: str
    start_time: datetime
    end_time: datetime
