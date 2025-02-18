from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_extract_criteria():
    response = client.post("/extract-criteria", 
                           files={"file": 
                                  ("test.pdf", 
                                   open("samples/job_descriptions/senior-data-analyst.pdf", "rb"))})
    assert response.status_code == 200
    assert "criteria" in response.json()


    print(response.json())

    with open("samples/criteria/criteria_test.json", "w") as f:
        json.dump(response.json(), f)

if __name__ == "__main__":
    test_extract_criteria()