import pytest
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
    return response.json().get("access_token")


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