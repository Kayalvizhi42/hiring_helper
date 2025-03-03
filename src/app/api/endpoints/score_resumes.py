from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.services.file_processing import process_file
from app.services.json_processing import process_json
from app.services.text_extraction import extract_text
from app.services.scoring import score_resume
from app.utils.format_table import flatten_job_match_score, format_as_csv


router = APIRouter()

@router.post("/score-resumes", response_class=FileResponse)
async def score_resumes(
    criteria_file: UploadFile = File(...),
    resume_files: list[UploadFile] = File(...)):
    """
    Scores multiple resumes against the provided ranking criteria and returns a CSV file.

    This endpoint accepts a JSON file containing job ranking criteria (e.g., required skills, experience)
    and evaluates multiple resume files (PDF or DOCX) against those criteria. The final results are 
    returned as a downloadable CSV file.

    Args:
        criteria_file (UploadFile): 
            - A JSON file containing the ranking criteria.
            - Must be a valid JSON file with key attributes.
            - Example format:
                ```json
                {
                    "title": "Data Scientist",
                    "skills": ["Python", "Machine Learning", "NLP"],
                    "experience": 3
                }
                ```
        
        resume_files (List[UploadFile]): 
            - A list of uploaded resume files to be evaluated.
            - Supported formats: PDF, DOCX.

    Processing Steps:
        - Parses the JSON criteria.
        - Extracts text from each resume.
        - Scores resumes based on matching criteria.
        - Flattens the structured results into a tabular format.
        - Converts the final scores into a downloadable CSV.

    Returns:
        StreamingResponse: A CSV file containing the scores for each resume.

    Example:
        **Request:**
        - Upload `criteria.json`
        - Upload `resume1.pdf`, `resume2.docx`

        **Response (CSV Download Example Content):**
        ```
        resume_file,score,matched_skills,missing_skills
        resume1.pdf,85,Python;Machine Learning,NLP
        resume2.docx,70,Python,Machine Learning;NLP
        ```

    """
    criteria: dict = await process_json(criteria_file)
    items = []

    for file in resume_files:
        file_content , file_extention = await process_file(file)
        text = extract_text(file_content, file_extention)
        result = await score_resume(criteria, text)
        item = flatten_job_match_score(result)
        items.append(item)

        
    return format_as_csv(items) 