import pytest
from server import create_app
from flask import json

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_add_and_get_books(client):
    # First register and login to get a token
    client.post("/api/auth/register", json={
        "name": "Book Tester",
        "email": "booktester@example.com",
        "password": "testpass"
    })

    login_res = client.post("/api/auth/login", json={
        "email": "booktester@example.com",
        "password": "testpass"
    })
    assert login_res.status_code == 200
    token = login_res.get_json()["token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Add a new book
    add_res = client.post("/api/books", json={
        "title": "Test Book",
        "author": "Test Author",
        "description": "This is a test book.",
        "condition": "Good"
    }, headers=headers)
    assert add_res.status_code == 201
    added_book = add_res.get_json()
    assert added_book["title"] == "Test Book"

    # Get my books
    my_books_res = client.get("/api/books/mine", headers=headers)
    assert my_books_res.status_code == 200
    my_books = my_books_res.get_json()
    assert any(b["title"] == "Test Book" for b in my_books)

    # Get all books
    all_books_res = client.get("/api/books/all", headers=headers)
    assert all_books_res.status_code == 200
    all_books = all_books_res.get_json()
    assert isinstance(all_books, list)
