from models.room import Room
from models.booking import Booking
from datetime import datetime

class RoomDB:
    def add_room(self, room: Room):
        pass

    def get_room_by_id(self, id: int) -> Room|None:
        pass


class MockRoomDB(RoomDB):
    rooms = [
        Room(id = 1, name = "room1", size = "S"),
        Room(id = 2, name = "room2", size = "L", is_vip=True)
    ]

    def add_room(self, room: Room):
        for r in self.rooms:
            if r.id == room.id:
                raise ValueError
        self.rooms.append(room)

    def get_room_by_id(self, id: int) -> Room|None:
        for r in self.rooms:
            if r.id == id:
                return r
        return None
    
class BookingDB:
    def create_booking(self, booking : Booking):
        pass

    def find_close_rooms(self, start_time : datetime, end_time : datetime) -> list[id]:
        pass

class MockBookingDB(BookingDB):
    def __init__(self):
        self.bookings = []

    def create_booking(self, booking : Booking):
        self.bookings.append(booking)

    def find_close_rooms(self, start_time : datetime, end_time : datetime) -> list[id]:
        res = []
        for booking in self.bookings:
            if start_time <= booking.start_time >= end_time or start_time <= booking.end_time >= end_time:
                res.append(booking.room_id)

        return res

# SOLID разработка  

# Boooking 
# .......|>>>>>|
# Хотим
# ..........|>>>>>|