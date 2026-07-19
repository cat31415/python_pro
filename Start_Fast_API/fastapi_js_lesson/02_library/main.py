from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Shelf API",
    description="Задание: каталог и избранное по контракту из TASK.md",
    version="1.0.0",
)

# TODO: добавьте books и favorite_ids из TASK.md.
# TODO: создайте FavoriteCreate.
# TODO: реализуйте семь вариантов запросов из таблицы контракта.


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", include_in_schema=False)
def catalog_page():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/favorites", include_in_schema=False)
def favorites_page():
    return FileResponse(FRONTEND_DIR / "favorites.html")

