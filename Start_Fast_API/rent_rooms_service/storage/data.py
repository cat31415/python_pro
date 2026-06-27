from models.room import Room
from models.booking import Booking


class RoomDB: 
    pass

class MockRoomDB(RoomDB):
    rooms = [
        Room(id = 1, name = "room1", size = "small"),
        Room(id = 2, name = "room2", size = "large", is_vip=True)
    ]

    def add_room(self, room: Room):
        for r in self.rooms:
            if r.id == room.id:
                raise ValueError
        self.rooms.append(room)

    def get_room_by_id(self, id: int) -> Room:
        for r in self.rooms:
            if r.id == id:
                return r
    
class BookingDB:
    pass

class MockBookingDB(BookingDB):
    bookings = []

    def create_booking(booking : Booking):
        booking.append(booking) 