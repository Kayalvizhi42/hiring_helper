from fastapi.testclient import TestClient
from app.main import app
import json
import csv 
import io

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
    assert response.headers.get("content-type") == "text/csv", "Content-Type is not text/csv"
    

    csv_content = response.content.decode("utf-8")
    csv_file = io.StringIO(csv_content)
    reader = csv.reader(csv_file)
        
    # Get all rows from the CSV
    rows = list(reader)

    assert len(rows) > 0, "CSV file is empty"

    print("CSV download test passed successfully.")

if __name__ == "__main__":
    test_score_resumes()