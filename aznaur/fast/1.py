from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

books = [
  { "id": 1, "title": "Мастер и Маргарита", "author": "Михаил Булгаков", "year": 1967 },
  { "id": 2, "title": "Преступление и наказание", "author": "Фёдор Достоевский", "year": 1866 },
  { "id": 3, "title": "Война и мир", "author": "Лев Толстой", "year": 1869 },
  { "id": 4, "title": "Евгений Онегин", "author": "Александр Пушкин", "year": 1833 },
  { "id": 5, "title": "Мёртвые души", "author": "Николай Гоголь", "year": 1842 },
  { "id": 6, "title": "Отцы и дети", "author": "Иван Тургенев", "year": 1862 },
  { "id": 7, "title": "Вишнёвый сад", "author": "Антон Чехов", "year": 1904 }
]


@app.get("/books")
def bok():
    return{"bok": books}

@app.get("/books/{book_id}")
def bokk(book_id: int):
    for bo in books:
        if bo["id"] == book_id:
            return bo
        
@app.get("/books/{year}")
def book_year(year: int):
    start_year, stop_year = map(int, year.split("-"))
    a = []
    for bok in books:
        if bok["year"] < stop_year and bok["year"] > start_year:
            a.append(bok)
    return a

