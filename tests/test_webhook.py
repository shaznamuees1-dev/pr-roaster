from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "PR Roaster is running"}

def test_reviews_endpoint():
    response = client.get("/reviews")
    assert response.status_code == 200
    assert isinstance(response.json(), list)