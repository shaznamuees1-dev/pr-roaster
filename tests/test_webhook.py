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

def test_webhook_invalid_signature():
    response = client.post(
        "/webhook",
        json={"action": "opened"},
        headers={"X-Hub-Signature-256": "sha256=invalid", "X-GitHub-Event": "pull_request"}
    )
    assert response.status_code == 401