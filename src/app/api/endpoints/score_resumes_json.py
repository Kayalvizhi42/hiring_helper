from fastapi import APIRouter, Form, UploadFile, File
from app.services.file_processing import process_file
from app.services.text_extraction import extract_text
from app.services.scoring import score_resume


router = APIRouter()

@router.post("/score-resumes-json")
async def score_resumes(
    criteria: str = Form(...),  # will be provided as a JSON string
    files: list[UploadFile] = File(...)):
    """
    Scores multiple resumes against the provided ranking criteria.

    Args:
        criteria (List[str]): A list of ranking criteria (e.g., skills, certifications).
        files (List[UploadFile]): A list of uploaded resume files (PDF or DOCX).

    Returns:
        A json file containing the scores for each resume.
    """
    results = []

    for file in files:
        file_content , file_extention = await process_file(file)
        text = extract_text(file_content, file_extention)
        result = score_resume(criteria, text)
        results.append(result)
        
    return {"results" : results}