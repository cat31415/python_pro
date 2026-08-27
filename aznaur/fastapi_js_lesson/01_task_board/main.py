from pathlib import Path
import psycopg2
from pydantic import BaseModel
import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, String, select, true
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, session


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI( 
    title="Task Board API",
    description="Задание: реализуйте API по контракту из TASK.md",
    version="1.0.0",
)

DB_CONFIG = {
    "dbname": "bit22",
    "user": "postgres",
    "password": "pass",
    "host": "localhost", 
    "port": "5432",
}

ORDER_COLUMNS =  (
    "id",
    "title",
    "priority",
    "done",
)

class BaseSql(DeclarativeBase):
    pass

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:pass@localhost:5432/bit22",
)

class Tasck(BaseSql):

    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    priority: Mapped[str] = mapped_column(String(50))
    done: Mapped[bool] = mapped_column(default=False)

engine = create_engine(DATABASE_URL, echo=True)



# TODO: создайте список tasks с 1–2 стартовыми задачами.
# TODO: создайте модели TaskCreate и TaskUpdate.
# TODO: добавьте четыре API-маршрута из TASK.md выше блока со статикой.

data = [
    {"id" : 1, "title": "Повторить модели Pydantic",  "priority": "high", "done": False},
]

class TaskCreate(BaseModel):
    title: str
    priority: str
    done: bool = False

def connect_to_db():
    """Открывает новое соединение с PostgreSQL."""

    return psycopg2.connect(**DB_CONFIG)
 
def row_to_task(row: tuple) -> dict:
    """Превращает строку PostgreSQL из tuple в словарь задачи."""

    return dict(zip(ORDER_COLUMNS, row))

def task_to_dict(task: Tasck) -> dict:

    return {
        "id": task.id,
        "title": task.title,
        "priority": task.priority,
        "done": task.done,
    }


def select_tasks(task_id: int):
    with session(engine) as session:
        task = session.get(Tasck, task_id)
        return task_to_dict(task) if task else None

def select_done_order_by_task():
    with session(engine) as session:
        tasks = session.scalars(
            select(Tasck).where(Tasck.done == True).order_by(Tasck.id)
        ).all() 
        return [task_to_dict(task) for task in tasks]


def select_tasks():

    with session(engine) as session:
        task = session.scalars(select(Tasck)). all()
        return task



def insert_task(
    title: str, 
    priority: str, 
    done: bool
    ):

    try:
        with session(engine) as session:
            task = Tasck(
                title = title,
                priority = priority,
                done = done)

            session.add(task)
            session.commit()

        return task
    except Exception:
        raise




def delete_task(task_id: int):
    pass

    


@app.get("/api/tasks")
def get_data():
    return {"items": select_tasks()}


@app.post("/api/tasks")
def create_task(task: TaskCreate):
    return insert_task(
        title=task.title,
        priority=task.priority,
        done=task.done
    )

@app.patch("/api/tasks/{task_id}")
def update_task(task_id: int):
    pass

@app.delete("/api/tasks/{task_id}")
def delete(task_id: int):
    return delete_task(task_id=task_id)




app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(FRONTEND_DIR / "index.html") 

