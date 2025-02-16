from fastapi import APIRouter, File, UploadFile
from app.services.file_processing import process_file
from app.services.text_extraction import extract_text
from app.services.scoring import extract_criteria

router = APIRouter()

@router.post("/extract-criteria")
async def extract_ranking_criteria(file: UploadFile = File(...)):
    file_content = await process_file(file)
    text = extract_text(file_content)
    criteria = extract_criteria(text)
    return {"criteria": criteria}