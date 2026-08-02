from pathlib import Path

import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Coffee Queue API",
    description="Учебный пример связи FastAPI, PostgreSQL и JavaScript",
    version="2.0.0",
)



DB_CONFIG = {
    "dbname": "bit",
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

    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT id, customer, drink_id, drink_name, price, status
            FROM coffee_orders
            ORDER BY id;
            """
        )
        rows = cursor.fetchall()
        return [row_to_order(row) for row in rows]
    finally:
        # Курсор и соединение нужно закрывать даже при ошибке.
        cursor.close()
        connection.close()


def insert_order(
    customer: str,
    drink_id: int,
    drink_name: str,
    price: int,
) -> dict:
    """Выполняет INSERT и возвращает созданную строку."""

    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO coffee_orders (
                customer,
                drink_id,
                drink_name,
                price,
                status
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, customer, drink_id, drink_name, price, status;
            """,
            (customer, drink_id, drink_name, price, "waiting"),
        )
        row = cursor.fetchone()

        if row is None:
            raise RuntimeError("PostgreSQL не вернул созданный заказ")

        # INSERT окончательно сохраняется только после commit().
        connection.commit()
        return row_to_order(row)
    except Exception:
        # Если запрос завершился ошибкой, отменяем незавершённую транзакцию.
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


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
