from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_dashboard_requires_authentication():
    response = client.get("/dashboard/")
    assert response.status_code in [401, 403]