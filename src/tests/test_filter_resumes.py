from fastapi.testclient import TestClient
from app.main import app
import io
import pandas as pd

client = TestClient(app)


def test_filter_resumes():
    response = client.post("/filter-resumes",
                          params={"user_query": "Show top 2 candidates with SQL and Python experience."},
                          files={"resume_scores": 
                                  ("job_match_score.csv", 
                                   open("samples/output/job_match_score.csv", "rb"))})
    
    assert response.status_code == 200, response.json()

    assert response.headers["content-type"].startswith("text/csv"), response.headers["content-type"]

    response.content.decode()

    # Read the CSV content
    csv_content = response.content.decode("utf-8")

    # Parse CSV using csv.reader
    df = pd.read_csv(io.StringIO(csv_content))

    # Ensure it has at least a header and one row
    assert not df.empty, "CSV file is empty"

    print(df)
    print("------------------------------------------")
    print("CSV download test passed successfully.")

if __name__ == "__main__":
    test_filter_resumes()