from fastapi import APIRouter
from fastapi import HTTPException

from models.booking import Booking
from models.room import Room
from services.booking_service import BookingService
from storage.data import MockBookingDB, MockRoomDB
from datetime import datetime

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

room_db = MockRoomDB()
booking_db = MockBookingDB() 

service = BookingService(room_db = room_db, booking_db = booking_db)

@router.get("")
def get_bookings():
    return service.get_bookings()

@router.post("")
def post_booking(booking : Booking):
    return service.create_booking(
        booking.room_id,
        booking.user_name,
        booking.start_time,
        booking.end_time
        )

@router.post("add_room")
def add_room():
    pass

@router.get("rooms")
def get_rooms():
    pass

