from fastapi import APIRouter, UploadFile, File
from app.services.file_processing import process_file
from app.services.text_extraction import extract_text
from app.services.scoring import score_resume
from app.services.json_processing import process_json


router = APIRouter()

@router.post("/score-resumes-json")
async def score_resumes(
    criteria_file: UploadFile = File(...),
    resume_files: list[UploadFile] = File(...)):
    """
    Scores multiple resumes against the provided ranking criteria.

    This endpoint processes a JSON file containing job ranking criteria (e.g., required skills, certifications) 
    and evaluates multiple resume files (PDF or DOCX) based on those criteria. 

    Args:
        criteria_file (UploadFile): 
            - A JSON file containing the ranking criteria.
            - Must have a valid JSON structure.
            - Example format:
                ```json
                {
                    "title": "Software Engineer",
                    "skills": ["Python", "Machine Learning", "FastAPI"],
                    "experience": 3
                }
                ```
        
        resume_files (List[UploadFile]): 
            - A list of resume files to be scored.
            - Supported formats: PDF, DOCX.

    Returns:
        Dict[str, List[Dict[str, any]]]: A dictionary containing scores for each processed resume.

    Example:
        **Request:**
        - Upload `criteria.json`
        - Upload `resume1.pdf`, `resume2.docx`

        **Response:**
        ```json
        {
            "results": [
                {
                    "resume": "resume1.pdf",
                    "score": 85,
                    "matched_skills": ["Python", "Machine Learning"]
                },
                {
                    "resume": "resume2.docx",
                    "score": 70,
                    "matched_skills": ["FastAPI"]
                }
            ]
        }
        ```
    """

    criteria: dict = await process_json(criteria_file)
    results = []

    for file in resume_files:
        file_content , file_extention = await process_file(file)
        text = extract_text(file_content, file_extention)
        result = await score_resume(criteria, text)
        results.append(result)
        
    return {"results" : results}