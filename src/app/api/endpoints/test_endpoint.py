from fastapi import APIRouter, HTTPException
from app.services.format_table import flatten_job_match_score, format_as_csv
from app.models.resume_score_model import JobMatchScore
import json
import os

router = APIRouter()

@router.get("/test-endpoint")
async def score_resumes():
    """

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    file_path = "samples/resume_score/resume_score_test.json"
    
    # Ensure the file is not empty
    if os.path.getsize(file_path) == 0:
        raise HTTPException(status_code=400, detail="JSON file is empty")
    
    with open(file_path, "r") as f:
        results: dict = json.load(f)

    items = []
    
    for result in results['results']:
        result = JobMatchScore.model_validate(result)
        item = flatten_job_match_score(result)
        items.append(item)

    print(items)
        
    return format_as_csv(items) 