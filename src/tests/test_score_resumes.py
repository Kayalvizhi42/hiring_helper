from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)


def test_score_resumes():

    with open("samples/criteria/response_1739761650980.json") as f:
        criteria = json.load(f)
    
    # Convert criteria to a JSON string for the form data
    criteria_json = json.dumps(criteria)

    response = client.post(
        "/score-resumes",
        data={"criteria": criteria_json},
        files={
            ("files", ("john_doe.pdf", open("samples/resumes/john_doe.pdf", "rb"), "application/pdf")),
            ("files", ("jane_smith.pdf", open("samples/resumes/jane_smith.pdf", "rb"), "application/pdf")),
            ("files", ("machel_johnson.pdf", open("samples/resumes/michael_johnson.pdf", "rb"), "application/pdf")),
        },

    )
    print(response.json())
    assert response.status_code == 200
    assert "results" in response.json()

    print(response.json())


if __name__ == "__main__":
    test_score_resumes()
