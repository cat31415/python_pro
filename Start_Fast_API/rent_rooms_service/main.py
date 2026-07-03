from services.booking_service import BookingService
from storage.data import MockBookingDB, MockRoomDB
from datetime import datetime
from routers.booking_router import router
from fastapi import FastAPI

app = FastAPI(title="Gaming rooms bookings")

app.include_router(router)