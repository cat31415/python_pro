from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_rooms_and_booking_rules():
    rooms_response = client.get("/api/rooms")
    assert rooms_response.status_code == 200
    rooms = rooms_response.json()["items"]
    assert len(rooms) >= 3
    room = rooms[0]

    first_response = client.post(
        "/api/bookings",
        json={
            "room_id": room["id"],
            "employee": "Тестовый пользователь",
            "date": "2099-12-31",
            "start_hour": 9,
            "duration_hours": 2,
        },
    )
    assert first_response.status_code == 201
    first = first_response.json()
    assert first["room_name"] == room["name"]

    conflict_response = client.post(
        "/api/bookings",
        json={
            "room_id": room["id"],
            "employee": "Другой пользователь",
            "date": "2099-12-31",
            "start_hour": 10,
            "duration_hours": 1,
        },
    )
    assert conflict_response.status_code == 409

    adjacent_response = client.post(
        "/api/bookings",
        json={
            "room_id": room["id"],
            "employee": "Следующая встреча",
            "date": "2099-12-31",
            "start_hour": 11,
            "duration_hours": 1,
        },
    )
    assert adjacent_response.status_code == 201
    adjacent = adjacent_response.json()

    schedule_response = client.get("/api/bookings", params={"date": "2099-12-31"})
    assert schedule_response.status_code == 200
    schedule = schedule_response.json()["items"]
    assert [item["start_hour"] for item in schedule] == sorted(item["start_hour"] for item in schedule)

    for booking_id in (first["id"], adjacent["id"]):
        delete_response = client.delete(f"/api/bookings/{booking_id}")
        assert delete_response.status_code == 204


def test_booking_validation_and_not_found():
    invalid_time_response = client.post(
        "/api/bookings",
        json={
            "room_id": 1,
            "employee": "Тест",
            "date": "2099-12-30",
            "start_hour": 7,
            "duration_hours": 1,
        },
    )
    assert invalid_time_response.status_code == 422

    late_response = client.post(
        "/api/bookings",
        json={
            "room_id": 1,
            "employee": "Тест",
            "date": "2099-12-30",
            "start_hour": 18,
            "duration_hours": 2,
        },
    )
    assert late_response.status_code == 422

    missing_room_response = client.post(
        "/api/bookings",
        json={
            "room_id": 999999,
            "employee": "Тест",
            "date": "2099-12-30",
            "start_hour": 10,
            "duration_hours": 1,
        },
    )
    assert missing_room_response.status_code == 404

