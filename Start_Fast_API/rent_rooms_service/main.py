from services.booking_service import BookingService
from storage.data import MockBookingDB, MockRoomDB
from datetime import datetime

room_db = MockRoomDB()
booking_db = MockBookingDB()

service = BookingService(room_db, booking_db)

service.add_room(3, "CS:GO", 'S')
service.create_booking(1, "Kirill", datetime(2026, 7, 29, 14, 30), datetime(2026, 7, 29, 15, 30))

print(service.room_db.rooms)
print(service.booking_db.bookings)