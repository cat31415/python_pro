from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Roomly API",
    description="Задание: бронирование без пересечений по контракту из TASK.md",
    version="1.0.0",
)

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

