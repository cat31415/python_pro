from routers.booking_router import router
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Gaming rooms bookings")

app.mount("/static", StaticFiles(directory=BASE_DIR / "ui" / "static"), name="static")
app.include_router(router)


@app.get("/")
def index():
    return FileResponse(BASE_DIR / "ui" / "templates" / "index.html")
