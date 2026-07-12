from datetime import datetime
from pydantic import BaseModel
import storage.data as db
from models.booking import Booking
from models.room import Room

class BookingService:

    def __init__(self, room_db : db.RoomDB, booking_db : db.BookingDB):
        self.room_db = room_db
        self.booking_db = booking_db

    def create_booking(
                self, 
                room_id : int,
                user_name : str,
                start_time : datetime,
                end_time : datetime
                ):
        
        if start_time < datetime.now():
            raise ValueError("Can't book room in the past")

        
        if start_time >= end_time:
            raise ValueError("End time can't be les or equal then start_time")
        
        if self.room_db.get_room_by_id(room_id) == None:
            raise ValueError("Don't have room with that id")
        
        closed_rooms = self.booking_db.find_close_rooms(start_time, end_time)

        if room_id in closed_rooms:
            raise ValueError("Room is alreade booked in that time")
        
        new_booking = Booking(room_id = room_id, user_name=user_name, start_time = start_time, end_time = end_time)

        self.booking_db.create_booking(new_booking)

    def add_room(
            self, 
            id: int,
            name: str,
            size: str,
            is_vip: bool = False
            ):

        if self.room_db.get_room_by_id(id) != None:
            raise ValueError("Room with this id is alreade in data base")
        
        new_room = Room(id = id, name = name, size = size, is_vip = is_vip)
        self.room_db.add_room(new_room)

    def get_bookings(self):
        return self.booking_db.get_bookings()
    
    def get_rooms(self):
        return self.room_db.get_rooms()


            
 
