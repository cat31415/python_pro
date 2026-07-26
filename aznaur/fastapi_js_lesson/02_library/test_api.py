from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_catalog_search_and_genres():
    list_response = client.get("/api/books")
    assert list_response.status_code == 200
    data = list_response.json()
    assert data["total"] == len(data["items"])
    assert len(data["items"]) >= 4

    first_book = data["items"][0]
    word = first_book["title"].split()[0].lower()
    search_response = client.get("/api/books", params={"query": word})
    assert search_response.status_code == 200
    assert any(book["id"] == first_book["id"] for book in search_response.json()["items"])

    genres_response = client.get("/api/genres")
    assert genres_response.status_code == 200
    assert first_book["genre"] in genres_response.json()["items"]

    genre_response = client.get("/api/books", params={"genre": first_book["genre"]})
    assert genre_response.status_code == 200
    assert all(book["genre"].lower() == first_book["genre"].lower() for book in genre_response.json()["items"])


def test_favorite_lifecycle_and_errors():
    books = client.get("/api/books").json()["items"]
    book = books[-1]

    client.delete(f"/api/favorites/{book['id']}")

    create_response = client.post("/api/favorites", json={"book_id": book["id"]})
    assert create_response.status_code == 201
    assert create_response.json()["id"] == book["id"]

    duplicate_response = client.post("/api/favorites", json={"book_id": book["id"]})
    assert duplicate_response.status_code == 409

    favorites_response = client.get("/api/favorites")
    assert favorites_response.status_code == 200
    assert any(item["id"] == book["id"] for item in favorites_response.json()["items"])

    delete_response = client.delete(f"/api/favorites/{book['id']}")
    assert delete_response.status_code == 204
    assert delete_response.content == b""

    missing_response = client.post("/api/favorites", json={"book_id": 999999})
    assert missing_response.status_code == 404

