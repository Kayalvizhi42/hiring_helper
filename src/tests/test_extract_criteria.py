from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_extract_criteria():
    response = client.post("/extract-criteria", 
                           files={"file": 
                                  ("test.pdf", 
                                   open("samples/job_descriptions/sample-job-description.pdf", "rb"))})
    assert response.status_code == 200
    assert "criteria" in response.json()

    print(response.json())

if __name__ == "__main__":
    test_extract_criteria()