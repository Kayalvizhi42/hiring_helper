from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)


def test_score_resumes():

    with open("samples/criteria/criteria_test.json") as f:
        criteria = json.load(f)
    
    # Convert criteria to a JSON string for the form data
    criteria_json = json.dumps(criteria)

    response = client.post(
        "/score-resumes",
        data={"criteria": criteria_json},
        files={
            ("files", ("john_doe.pdf", open("samples/resumes/weak-fit.pdf", "rb"), "application/pdf")),
            ("files", ("jane_smith.pdf", open("samples/resumes/moderate-fit.pdf", "rb"), "application/pdf")),
            ("files", ("machel_johnson.pdf", open("samples/resumes/strong-fit.pdf", "rb"), "application/pdf")),
        },

    )
    assert response.status_code == 200
    assert "results" in response.json()

    print(response.json())

    with open("samples/resume_score/resume_score_test.json", "w") as f:
        json.dump(response.json(), f)

if __name__ == "__main__":
    test_score_resumes()
