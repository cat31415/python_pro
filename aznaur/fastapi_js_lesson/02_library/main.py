from pathlib import Path
import os 

from fastapi import FastAPI 
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, select, delete, update, VARCHAR, String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, session


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Shelf API",
    description="Задание: каталог и избранное по контракту из TASK.md",
    version="1.0.0",
)

class Base(DeclarativeBase):
    pass

class Books(Base):

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(100))
    genre: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(String(10))
    description: Mapped = mapped_column(String(500))

class Favorite(Base):

    __tablename__ = "favorite"

    favorite_ids: Mapped[int] = mapped_column(String(100))

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:pass@localhost:5432/bit22",
)
engine = create_engine(DATABASE_URL, echo=True)

# TODO: добавьте books и favorite_ids из TASK.md.
# TODO: создайте FavoriteCreate.
# TODO: реализуйте семь вариантов запросов из таблицы контракта.



def get_genres():
    with session(engine) as sessiion:
        genre = sessiion.scalar(select(Books.genre))
        return genre



def get_books(): 
    with session(engine) as sessioon:
        bok = sessioon.scalars(select(Books)).all()
        return bok
        
def delete_favorites():
    with session(engine) as sessioon:
        bok = sessioon.scalars(select(Books)).all()
        return bok           

def get_favorites(): 
    with session(engine) as sessioon:
        bok = sessioon.scalars(select(Favorite)).all()

@app.get("/api/genres")
def get_genres():
    return {"items": get_genres()}

@app.get("/api/books")
def get_bookss():
    return {"items" : get_books()}

@app.get("/api/")
def get_():
    pass

@app.get("/api/")
def get__():
    pass

@app.get("/api/favorites")
def get_favorites():
    pass

@app.post("/api/favorites")
def post_favorites():
    pass

@app.delete("/api/favorites/{book_id}")
def delete_favorites():
    pass
 
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", include_in_schema=False)
def catalog_page():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/favorites", include_in_schema=False)
def favorites_page():
    return FileResponse(FRONTEND_DIR / "favorites.html")

