import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# Registracija i login jer svi POST endpointi zahtijevaju login

def get_token():
    # Registracija
    client.post("/auth/register", json={
        "email": "test_forum@test.com",
        "full_name": "Test User",
        "password": "test1234"
    })
    # Login
    response = client.post("/auth/login", data={
        "username": "test_forum@test.com",
        "password": "test1234"
    })

    assert response.status_code == 200
    token = response.json().get("access_token")
    assert token is not None
    return token

def create_test_topic(token):
    unique_title = f"Test tema {uuid.uuid4()}"

    response = client.post("/forum/topics", json={
        "title": unique_title,
        "content": "Ovo je test sadrzaj teme.",
        "category_id": 1,
        "tags": []
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201
    return response.json()

# Testovi za kreiranje teme 

def test_create_topic_success():
    token = get_token()
    response = client.post("/forum/topics", json={
        "title": "Test tema naslov",
        "content": "Ovo je sadrzaj test teme.",
        "category_id": 1,
        "tags": []
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test tema naslov"


def test_create_topic_without_auth():
    response = client.post("/forum/topics", json={
        "title": "Test tema",
        "content": "Sadrzaj teme.",
        "category_id": 1,
        "tags": []
    })
    assert response.status_code == 401


def test_create_topic_missing_fields():
    token = get_token()
    response = client.post("/forum/topics", json={
        "title": "",
        "content": "",
        "category_id": 1
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [400, 422]


# Testovi za komentare

def test_create_comment_success():
    token = get_token()
    # Kreiraj temu
    topic_response = client.post("/forum/topics", json={
        "title": "Tema za komentar test",
        "content": "Sadrzaj teme za testiranje komentara.",
        "category_id": 1,
        "tags": []
    }, headers={"Authorization": f"Bearer {token}"})
    assert topic_response.status_code == 201
    topic_id = topic_response.json()["id"]

    # Kreiraj komentar
    response = client.post("/forum/comments", json={
        "content": "Ovo je test komentar.",
        "topic_id": topic_id
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["content"] == "Ovo je test komentar."


def test_create_comment_without_auth():
    response = client.post("/forum/comments", json={
        "content": "Komentar bez autorizacije.",
        "topic_id": 1
    })
    assert response.status_code == 401


def test_get_comments_for_topic():
    response = client.get("/forum/topics/1/comments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_forum_root():
    response = client.get("/forum/")
    assert response.status_code == 200


def test_get_categories():
    response = client.get("/forum/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_all_topics():
    response = client.get("/forum/topics")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "items" in data
    assert "page" in data
    assert "per_page" in data
    assert "total" in data
    assert isinstance(data["items"], list)


def test_get_topic_details_success():
    token = get_token()
    topic = create_test_topic(token)

    response = client.get(f"/forum/topics/{topic['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == topic["id"]
    assert response.json()["title"] == topic["title"]


def test_get_topic_details_not_found():
    response = client.get("/forum/topics/999999")
    assert response.status_code == 404


def test_increment_topic_view_success():
    token = get_token()
    topic = create_test_topic(token)

    response = client.patch(f"/forum/topics/{topic['id']}/view")

    assert response.status_code == 200


def test_increment_topic_view_not_found():
    response = client.patch("/forum/topics/999999/view")
    assert response.status_code == 404


def test_get_comments_for_new_topic_empty_list():
    token = get_token()
    topic = create_test_topic(token)

    response = client.get(f"/forum/topics/{topic['id']}/comments")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_comment_missing_content():
    token = get_token()
    topic = create_test_topic(token)

    response = client.post("/forum/comments", json={
        "content": "",
        "topic_id": topic["id"]
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code in [400, 422]


def test_delete_topic_without_auth():
    response = client.delete("/forum/topics/1")
    assert response.status_code == 401


def test_get_me_without_auth():
    response = client.get("/me")
    assert response.status_code == 401    