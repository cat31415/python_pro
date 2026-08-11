from pathlib import Path
import psycopg2
from pydantic import BaseModel

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException


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

def select_tasks():

    conect = connect_to_db()
    cursors = conect.cursor()

    try:
        cursors.execute(
            """
            SELECT id, title, priority, done
            FROM tasks 

            """
        )
        rows = cursors.fetchall()
        return [row_to_task(row) for row in rows]
    finally:
        cursors.close()
        conect.close()

def insert_task(title: str, priority: str, done: bool):

    conect = connect_to_db()
    cursors = conect.cursor()

    try:
        cursors.execute(
            """
            INSERT INTO tasks (
                title,
                priority,
                done
              )    VALUES (%s, %s, %s)
              RETURNING id, title, priority, done;
            """,
            (title, priority, done), 
        )
        row = cursors.fetchone()

        if row is None:
            raise RuntimeError("Ошибка при вставке задачи в базу данных.")

        conect.commit()
        return row_to_task(row)
    finally:
        cursors.close()
        conect.close()

def delete_task(task_id: int):
    conect = connect_to_db()
    cursors = conect.cursor()

    try:
        cursors.execute(
            """ 
            DELETE FROM tasks WHERE id = %s
               RETURNING id, title, priority, done;
            """,
            (task_id,)
            )
        row = cursors.fetchone()
        conect.commit()

        if row is None:
            return None
        return row_to_task(row)
    except Exception:
        conect.rollback()
        raise
    finally:    
        cursors.close()
        conect.close()

    


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

