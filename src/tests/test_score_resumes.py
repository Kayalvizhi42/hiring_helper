from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)


def test_score_resumes():

    response = client.post(
        "/score-resumes-json",
        files={
            ("resume_files", ("john_doe.pdf", open("samples/resumes/weak-fit.pdf", "rb"), "application/pdf")),
            ("resume_files", ("jane_smith.pdf", open("samples/resumes/moderate-fit.pdf", "rb"), "application/pdf")),
            ("resume_files", ("machel_johnson.pdf", open("samples/resumes/strong-fit.pdf", "rb"), "application/pdf")),
            ("criteria_file", ("criteria_test.json", open("samples/criteria/criteria_test.json", "rb"), "application/json"))
        },

    )

    assert response.status_code == 200
    assert "results" in response.json()

    
    with open("samples/resume_score/resume_score_test.json", "w") as f:
        json.dump(response.json(), f)

    print('------------------------------------------')
    print("Resume scoring test passed successfully.")

if __name__ == "__main__":
    test_score_resumes()
