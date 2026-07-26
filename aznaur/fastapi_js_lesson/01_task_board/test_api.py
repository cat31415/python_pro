from uuid import uuid4

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_task_lifecycle():
    title = f"Тестовая задача {uuid4().hex[:8]}"

    create_response = client.post(
        "/api/tasks",
        json={"title": title, "priority": "high"},
    )
    assert create_response.status_code == 201
    task = create_response.json()
    assert task["title"] == title
    assert task["priority"] == "high"
    assert task["done"] is False
    assert isinstance(task["id"], int)

    list_response = client.get("/api/tasks")
    assert list_response.status_code == 200
    assert any(item["id"] == task["id"] for item in list_response.json()["items"])

    update_response = client.patch(
        f"/api/tasks/{task['id']}",
        json={"done": True},
    )
    assert update_response.status_code == 200
    assert update_response.json()["done"] is True

    delete_response = client.delete(f"/api/tasks/{task['id']}")
    assert delete_response.status_code == 204
    assert delete_response.content == b""


def test_validation_and_not_found_errors():
    invalid_response = client.post(
        "/api/tasks",
        json={"title": "", "priority": "urgent"},
    )
    assert invalid_response.status_code == 422

    missing_response = client.patch(
        "/api/tasks/999999",
        json={"done": True},
    )
    assert missing_response.status_code == 404

