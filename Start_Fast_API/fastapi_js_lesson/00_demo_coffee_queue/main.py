from pathlib import Path

import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, select
from  sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Coffee Queue API",
    description="Учебный пример связи FastAPI, PostgreSQL и JavaScript",
    version="2.0.0",
)

DB_CONFIG = {
    "dbname": "coffee",
    "user": "postgres",
    "password": "pass",
    "host": "localhost",
    "port": "5432",
}

# Меню пока оставляем обычным Python-списком.
# В PostgreSQL на этом занятии хранится только очередь заказов.
drinks: list[dict] = [
    {"id": 1, "name": "Фильтр-кофе", "price": 170, "ready_minutes": 3},
    {"id": 2, "name": "Капучино", "price": 230, "ready_minutes": 6},
    {"id": 3, "name": "Какао", "price": 210, "ready_minutes": 5},
]

# PostgreSQL возвращает строку как tuple. Эти названия помогут превратить
# полученный tuple в словарь, который FastAPI затем отправит как JSON.



ORDER_COLUMNS = (
    "id",
    "customer",
    "drink_id",
    "drink_name",
    "price",
    "status",
)

class BaseAlchemy(DeclarativeBase):
    pass

class Order(BaseAlchemy):

    __tablename__ = "coffee_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer: Mapped[str] = mapped_column(String(30))
    drink_id: Mapped[int] 
    drink_name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int]
    status: Mapped[str] = mapped_column(String(20))

db_link = "postgresql+psycopg://postgres:pass@localhost:5432/coffee"
engine = create_engine(db_link, echo=True)

BaseAlchemy.metadata.create_all(engine)



class OrderCreate(BaseModel):
    customer: str = Field(min_length=2, max_length=30)
    drink_id: int


def connect_to_db():
    """Открывает новое соединение с PostgreSQL."""

    return psycopg2.connect(**DB_CONFIG)


def row_to_order(row: tuple) -> dict:
    """Превращает строку PostgreSQL из tuple в словарь заказа."""

    return dict(zip(ORDER_COLUMNS, row))


def select_orders() -> list[dict]:
    """Выполняет обычный SELECT и возвращает все заказы."""

    with Session(engine) as session:
        orders = session.scalars(select(Order)).all()
    
    return orders
   


def insert_order(
    customer: str,
    drink_id: int,
    drink_name: str,
    price: int,
) -> dict:
    """Выполняет INSERT и возвращает созданную строку."""

    try:
        with Session(engine) as session:
            order = Order(customer = customer,
                drink_id = drink_id,
                drink_name = drink_name,
                price = price,
                status = "waiting")

            session.add(order)
            session.commit()

        return order
    except Exception:
        raise



def update_order_status(order_id: int) -> dict | None:
    """Выполняет UPDATE и возвращает изменённую строку или None."""

    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE coffee_orders
            SET status = %s
            WHERE id = %s
            RETURNING id, customer, drink_id, drink_name, price, status;
            """,
            ("ready", order_id),
        )
        row = cursor.fetchone()
        connection.commit()

        if row is None:
            return None
        return row_to_order(row)
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


@app.get("/api/drinks", summary="Получить меню")
def get_drinks():
    return {"items": drinks}


@app.get("/api/orders", summary="Получить очередь заказов")
def get_orders():
    return {"items": select_orders()}


@app.post("/api/orders", status_code=201, summary="Создать заказ")
def create_order(payload: OrderCreate):
    drink = None
    
    for d in drinks:
        if d["id"] == payload.drink_id:
             drink = d

    if drink is None:
        raise HTTPException(status_code=404, detail="Напиток не найден")

    return insert_order(
        customer=payload.customer.strip(),
        drink_id=drink["id"],
        drink_name=drink["name"],
        price=drink["price"],
    )


@app.patch("/api/orders/{order_id}/ready", summary="Отметить заказ готовым")
def mark_order_ready(order_id: int):
    order = update_order_status(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.delete("/api/orders/{order_id}", summary="Удалить заказ")
def del_order(order_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM coffee_orders WHERE id = %s
            RETURNING id, customer, drink_id, drink_name, price, status;
            """,
            (order_id),
        )
        row = cursor.fetchone()
        connection.commit()

        if row is None:
            return None
        return row_to_order(row)
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
