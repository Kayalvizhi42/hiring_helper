from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_extract_criteria():
    response = client.post("/extract-criteria", files={"file": ("test.pdf", open("test.pdf", "rb"))})
    assert response.status_code == 200
    assert "criteria" in response.json()