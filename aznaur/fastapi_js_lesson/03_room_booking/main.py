from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import Select, create_engine, String, delete, update, JSON
from sqlalchemy.orm import Session, DeclarativeBase, mapped_column, Mapped

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Roomly API",
    description="Задание: бронирование без пересечений по контракту из TASK.md",
    version="1.0.0",
)

class Base(DeclarativeBase):
    pass

class Rooms(Base): 

    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    capacity: Mapped[int] = mapped_column(String(10))
    equipment: Mapped[list[any]] = mapped_column(JSON nullable=False, default=dict)

def task_to_dict(rom: Rooms) -> dict:

    return { 
        "id": rom.id, 
        "name": rom.name,
        "capacity": rom.capacity,
        "equipment": rom.equipment
    }




# TODO: добавьте rooms и bookings из TASK.md.
# TODO: создайте BookingCreate.
# TODO: реализуйте GET комнат, GET расписания, POST и DELETE бронирования.
# TODO: верните 409, если интервалы пересекаются.


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", include_in_schema=False)
def booking_page():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/schedule", include_in_schema=False)
def schedule_page():
    return FileResponse(FRONTEND_DIR / "schedule.html")

