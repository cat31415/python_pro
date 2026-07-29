import pytest
from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


@pytest.fixture(autouse=True)
def fake_database(monkeypatch):
    """Подменяет PostgreSQL обычным списком только на время теста."""

    orders = [
        {
            "id": 1,
            "customer": "Лена",
            "drink_id": 2,
            "drink_name": "Капучино",
            "price": 230,
            "status": "waiting",
        }
    ]

    def fake_select_orders():
        return [order.copy() for order in orders]

    def fake_insert_order(customer, drink_id, drink_name, price):
        order = {
            "id": max((item["id"] for item in orders), default=0) + 1,
            "customer": customer,
            "drink_id": drink_id,
            "drink_name": drink_name,
            "price": price,
            "status": "waiting",
        }
        orders.append(order)
        return order.copy()

    def fake_update_order_status(order_id):
        order = next(
            (item for item in orders if item["id"] == order_id),
            None,
        )
        if order is None:
            return None
        order["status"] = "ready"
        return order.copy()

    monkeypatch.setattr(main, "select_orders", fake_select_orders)
    monkeypatch.setattr(main, "insert_order", fake_insert_order)
    monkeypatch.setattr(main, "update_order_status", fake_update_order_status)


def test_frontend_is_served_by_fastapi():
    page_response = client.get("/")
    assert page_response.status_code == 200
    assert "Coffee Queue" in page_response.text

    script_response = client.get("/static/app.js")
    assert script_response.status_code == 200
    assert "fetch(path" in script_response.text


def test_demo_flow():
    menu_response = client.get("/api/drinks")
    assert menu_response.status_code == 200
    assert len(menu_response.json()["items"]) >= 3

    create_response = client.post(
        "/api/orders",
        json={"customer": "Тест", "drink_id": 1},
    )
    assert create_response.status_code == 201
    order = create_response.json()
    assert order["status"] == "waiting"

    ready_response = client.patch(f"/api/orders/{order['id']}/ready")
    assert ready_response.status_code == 200
    assert ready_response.json()["status"] == "ready"


def test_unknown_drink_returns_404():
    response = client.post(
        "/api/orders",
        json={"customer": "Тест", "drink_id": 9999},
    )
    assert response.status_code == 404


def test_unknown_order_returns_404():
    response = client.patch("/api/orders/9999/ready")
    assert response.status_code == 404
