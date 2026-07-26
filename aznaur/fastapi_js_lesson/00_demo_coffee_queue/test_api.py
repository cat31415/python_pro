from fastapi.testclient import TestClient

from main import app, orders


client = TestClient(app)


def test_frontend_is_served_by_fastapi():
    page_response = client.get("/")
    assert page_response.status_code == 200
    assert "Coffee Queue" in page_response.text

    script_response = client.get("/static/app.js")
    assert script_response.status_code == 200
    assert 'fetch(path' in script_response.text


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

    orders[:] = [item for item in orders if item["id"] != order["id"]]


def test_unknown_drink_returns_404():
    response = client.post(
        "/api/orders",
        json={"customer": "Тест", "drink_id": 9999},
    )
    assert response.status_code == 404
