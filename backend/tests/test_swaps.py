import pytest
from server import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def register_and_login(client, name, email, password="testpass"):
    client.post("/api/auth/register", json={
        "name": name,
        "email": email,
        "password": password
    })
    login_res = client.post("/api/auth/login", json={
        "email": email,
        "password": password
    })
    assert login_res.status_code == 200
    return login_res.get_json()["token"]

def add_book(client, token, title="Book Title", author="Book Author"):
    headers = {"Authorization": f"Bearer {token}"}
    res = client.post("/api/books", json={
        "title": title,
        "author": author,
        "condition": "Good"
    }, headers=headers)
    assert res.status_code == 201
    return res.get_json()["_id"]

def test_swap_flow(client):
    # Register two users
    token_owner = register_and_login(client, "Owner", "owner@example.com")
    token_requester = register_and_login(client, "Requester", "requester@example.com")

    # Owner adds a book
    owner_book_id = add_book(client, token_owner, title="Owner's Book")

    # Requester sends swap request
    headers_requester = {"Authorization": f"Bearer {token_requester}"}
    swap_res = client.post("/api/swap-requests", json={
        "requestedBookId": owner_book_id,
        "message": "I’d love to swap this!"
    }, headers=headers_requester)
    assert swap_res.status_code == 201
    swap = swap_res.get_json()
    swap_id = swap["_id"]

    # Requester can view their requests
    my_swaps_res = client.get("/api/swap-requests/requester", headers=headers_requester)
    assert my_swaps_res.status_code == 200
    my_swaps = my_swaps_res.get_json()
    assert any(s["_id"] == swap_id for s in my_swaps)

    # Owner can see swap request on their book
    headers_owner = {"Authorization": f"Bearer {token_owner}"}
    owner_swaps_res = client.get("/api/swap-requests/owner", headers=headers_owner)
    assert owner_swaps_res.status_code == 200
    owner_swaps = owner_swaps_res.get_json()
    assert any(s["_id"] == swap_id for s in owner_swaps)

    # Owner accepts the swap request
    respond_res = client.put(f"/api/swap-requests/{swap_id}/respond", json={
        "status": "accepted"
    }, headers=headers_owner)
    assert respond_res.status_code == 200
    assert "accepted" in respond_res.get_json()["message"]

    # After acceptance, requester should see updated status
    my_swaps_res2 = client.get("/api/swap-requests/requester", headers=headers_requester)
    statuses = [s["status"] for s in my_swaps_res2.get_json()]
    assert "accepted" in statuses
