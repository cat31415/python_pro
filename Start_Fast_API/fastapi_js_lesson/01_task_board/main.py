from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Task Board API",
    description="Задание: реализуйте API по контракту из TASK.md",
    version="1.0.0",
)

# TODO: создайте список tasks с 1–2 стартовыми задачами.
# TODO: создайте модели TaskCreate и TaskUpdate.
# TODO: добавьте четыре API-маршрута из TASK.md выше блока со статикой.


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(FRONTEND_DIR / "index.html")

