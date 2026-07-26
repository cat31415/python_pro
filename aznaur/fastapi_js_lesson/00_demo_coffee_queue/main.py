from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Coffee Queue API",
    description="Учебный пример связи FastAPI и JavaScript",
    version="1.0.0",
)

drinks: list[dict] = [
    {"id": 1, "name": "Фильтр-кофе", "price": 170, "ready_minutes": 3},
    {"id": 2, "name": "Капучино", "price": 230, "ready_minutes": 6},
    {"id": 3, "name": "Какао", "price": 210, "ready_minutes": 5},
]

orders: list[dict] = [
    {
        "id": 1,
        "customer": "Лена",
        "drink_id": 2,
        "drink_name": "Капучино",
        "price": 230,
        "status": "waiting",
    }
]


class OrderCreate(BaseModel):
    customer: str = Field(min_length=2, max_length=30)
    drink_id: int


@app.get("/api/drinks", summary="Получить меню")
def get_drinks():
    return {"items": drinks}


@app.get("/api/orders", summary="Получить очередь заказов")
def get_orders():
    return {"items": orders}


@app.post("/api/orders", status_code=201, summary="Создать заказ")
def create_order(payload: OrderCreate):
    drink = None

    for dr in drinks:
        if payload.drink_id == dr["id"]:
            drink = dr
            break

    if drink is None:
        raise HTTPException(status_code=404, detail="Напиток не найден")

    order = {
        "id": max((item["id"] for item in orders), default=0) + 1,
        "customer": payload.customer.strip(),
        "drink_id": drink["id"],
        "drink_name": drink["name"],
        "price": drink["price"],
        "status": "waiting",
    }
    orders.append(order)
    return order


@app.patch("/api/orders/{order_id}/ready", summary="Отметить заказ готовым")
def mark_order_ready(order_id: int):
    order = next((item for item in orders if item["id"] == order_id), None)
    if order is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    order["status"] = "ready"
    return order


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(FRONTEND_DIR / "index.html")

