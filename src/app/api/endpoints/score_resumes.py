from fastapi import APIRouter, Form, UploadFile, File
from app.services.file_processing import process_file
from app.services.text_extraction import extract_text
from app.services.scoring import score_resume
from app.services.format_table import flatten_job_match_score, format_as_csv

router = APIRouter()

@router.post("/score-resumes")
async def score_resumes(
    criteria: str = Form(...),  # will be provided as a JSON string
    files: list[UploadFile] = File(...)):
    """
    Scores multiple resumes against the provided ranking criteria.

    Args:
        criteria (List[str]): A list of ranking criteria (e.g., skills, certifications).
        files (List[UploadFile]): A list of uploaded resume files (PDF or DOCX).

    Returns:
        A downloadable csv containing the scores for each resume.
    """

    items = []

    for file in files:
        file_content , file_extention = await process_file(file)
        text = extract_text(file_content, file_extention)
        result = score_resume(criteria, text)
        item = flatten_job_match_score(result)
        items.append(item)

        
    return format_as_csv(items) 