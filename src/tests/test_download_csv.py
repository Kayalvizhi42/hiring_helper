from fastapi.testclient import TestClient
from app.main import app
import io
import pandas as pd

client = TestClient(app)


def test_score_resumes():
    response = client.post(
        "/score-resumes",
        files={
            ("resume_files", ("resume_1.pdf", open("samples/resumes/weak-fit.pdf", "rb"), "application/pdf")),
            ("resume_files", ("resume_2.pdf", open("samples/resumes/moderate-fit.pdf", "rb"), "application/pdf")),
            ("resume_files", ("resume_3.pdf", open("samples/resumes/strong-fit.pdf", "rb"), "application/pdf")),
            (
                "criteria_file",
                ("criteria_test.json", open("samples/criteria/criteria_test.json", "rb"), "application/json"),
            ),
        },
    )
    assert response.status_code == 200, response.json()

    assert response.headers["content-type"].startswith("text/csv"), response.headers["content-type"]
    assert 'attachment; filename="job_match_score.csv"' in response.headers.get("content-disposition", ""), (
        response.headers.get("content-disposition", "")
    )

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


def test_download_csv():
    response = client.get("/test-endpoint")

    assert response.status_code == 200, response.json()

    assert response.headers["content-type"].startswith("text/csv"), response.headers["content-type"]
    assert 'attachment; filename="job_match_score.csv"' in response.headers.get("content-disposition", ""), (
        response.headers.get("content-disposition", "")
    )

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
    # test_score_resumes()

    test_download_csv()
