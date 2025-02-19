from fastapi import UploadFile, HTTPException
import json

async def process_json(file: UploadFile) -> dict:
    try:
        contents = await file.read()
        criteria_data = json.loads(contents)  # Parse JSON

        return criteria_data
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in criteria file.")