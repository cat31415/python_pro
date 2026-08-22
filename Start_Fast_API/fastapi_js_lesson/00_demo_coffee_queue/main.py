import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, select, update, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Coffee Queue API",
    description="Учебный пример связи FastAPI, PostgreSQL и JavaScript",
    version="2.0.0",
)

# Меню пока оставляем обычным Python-списком.
# В PostgreSQL хранится только очередь заказов.
drinks: list[dict] = [
    {"id": 1, "name": "Фильтр-кофе", "price": 170, "ready_minutes": 3},
    {"id": 2, "name": "Капучино", "price": 230, "ready_minutes": 6},
    {"id": 3, "name": "Какао", "price": 210, "ready_minutes": 5},
]

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


# В Docker PostgreSQL работает в этом же контейнере, поэтому адрес — localhost.
# Через DATABASE_URL подключение можно изменить, не редактируя Python-код.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:pass@localhost:5432/coffee",
)

engine = create_engine(
    DATABASE_URL,
    echo=True,
)

# После запуска PostgreSQL SQLAlchemy сама создаст таблицу coffee_orders.
BaseAlchemy.metadata.create_all(engine)


class OrderCreate(BaseModel):
    customer: str = Field(min_length=2, max_length=30)
    drink_id: int


def order_to_dict(order: Order) -> dict:
    """Превращает объект SQLAlchemy в обычный словарь для JSON-ответа."""

    return {
        "id": order.id,
        "customer": order.customer,
        "drink_id": order.drink_id,
        "drink_name": order.drink_name,
        "price": order.price,
        "status": order.status,
    }


def select_orders() -> list[dict]:
    """Возвращает все заказы из PostgreSQL."""

    with Session(engine) as session:
        orders = session.scalars(select(Order).order_by(Order.id)).all()
        return [order_to_dict(order) for order in orders]


def select_order(order_id: int) -> dict | None:
    """Возвращает заказ по его ID из PostgreSQL."""

    with Session(engine) as session:
        order = session.get(Order, order_id)
        return order_to_dict(order) if order else None

def select_done_order_by_customer(customer: str) -> list[dict]:
    """Возвращает готовые заказы по имени клиента из PostgreSQL."""

    with Session(engine) as session:
        orders = session.scalars(
            select(Order).where(Order.customer == customer and Order.status == "ready").order_by(Order.id)
        ).all()
        return [order_to_dict(order) for order in orders]

def change_order_status(order_id: int, status: str) -> dict | None:
    """Меняет статус заказа."""

    with Session(engine) as session:
        order = session.get(Order, order_id)
        if order is None:
            return None

        order.status = status
        session.commit()
        return order_to_dict(order)

def change_order_status_by_customer(customer: str, status: str) -> list[dict]:
    """Меняет статус заказов по имени клиента."""

    with Session(engine) as session:
        # orders = session.scalars(
        #     select(Order).where(Order.customer == customer)
        # ).all()

        # for order in orders:
        #     order.status = status

        query_update = (update(Order).where(Order.customer == customer).values(status=status))
        session.execute(query_update)
        session.commit()
        return [order_to_dict(order) for order in session.scalars(select(Order).where(Order.customer == customer)).all()]

def delete_orders_by_id(id: int) -> dict | None:
    """Удаляет заказ по его ID из PostgreSQL."""

    with Session(engine) as session:
        order = session.get(Order, id)
        if order is None:
            return None

        result = order_to_dict(order)
        session.delete(order)
        session.commit()
        return result

def delete_done_orders_by_customer(customer: str) -> list[dict]:
    """Удаляет готовые заказы по имени клиента из PostgreSQL."""

    with Session(engine) as session:
        orders = session.scalars(
            select(Order).where(Order.customer == customer and Order.status == "ready")
        ).all()

        result = [order_to_dict(order) for order in orders]
        for order in orders:
            session.delete(order)
        session.commit()
        return result

def insert_order(
    customer: str,
    drink_id: int,
    drink_name: str,
    price: int,
) -> dict:
    """Добавляет заказ в PostgreSQL и возвращает его как словарь."""

    with Session(engine) as session:
        order = Order(
            customer=customer,
            drink_id=drink_id,
            drink_name=drink_name,
            price=price,
            status="waiting",
        )
        session.add(order)
        session.commit()
        return order_to_dict(order)


def update_order_status(order_id: int) -> dict | None:
    """Меняет статус заказа на ready или возвращает None."""

    with Session(engine) as session:
        order = session.get(Order, order_id)
        if order is None:
            return None

        order.status = "ready"
        session.commit()
        return order_to_dict(order)


def delete_order(order_id: int) -> dict | None:
    """Удаляет заказ из PostgreSQL или возвращает None."""

    with Session(engine) as session:
        order = session.get(Order, order_id)
        if order is None:
            return None

        result = order_to_dict(order)
        session.delete(order)
        session.commit()
        return result

        # query_delete = delete(Order).where(Order.id == order_id and Order.status == "ready")
        # session.execute(query_delete)
        # session.commit()


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
def del_order(order_id: int):
    order = delete_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order
