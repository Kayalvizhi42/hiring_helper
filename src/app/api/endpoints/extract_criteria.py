from fastapi import APIRouter, File, UploadFile
from app.services.file_processing import process_file
from app.services.text_extraction import extract_text
from app.services.scoring import extract_criteria

router = APIRouter()

@router.post("/extract-criteria")
async def extract_ranking_criteria(job_description: UploadFile = File(...)):
    """
    Extract ranking criteria from an uploaded job description file.

    This endpoint receives a job description file (e.g., PDF or DOCX) as input. It performs the following steps:
    
    1. **File Processing:**  
       The uploaded file is processed asynchronously by `process_file`, which returns the file's content and its extension.
    
    2. **Text Extraction:**  
       The raw file content is then passed to `extract_text` along with the file extension to extract the textual content.
    
    3. **Criteria Extraction:**  
       The extracted text is analyzed by the `extract_criteria` function, which identifies key ranking criteria from the job description.
    
    4. **Response:**  
       The endpoint returns a JSON object with the extracted criteria.

    Args:
        file (UploadFile): An uploaded file containing the job description (PDF or DOCX).

    Returns:
        dict: A dictionary with a single key "criteria" mapping to the extracted ranking criteria.
        
        Example:
            {
                "criteria": {
                    "job_title": "Software Engineer",
                    "technical_skills": ["Python", "FastAPI", "Docker"],
                    "soft_skills": ["Communication", "Teamwork"],
                    "experience_requirements": ["3+ years in software development"],
                    "education_requirements": ["Bachelor's degree in Computer Science"],
                    "nice_to_have": ["Experience with cloud platforms"],
                    ...
                }
            }

    Example Usage:
        Using cURL:
        ```
        curl -X POST "http://localhost:8000/extract-criteria" \
             -F "file=@/path/to/job_description.pdf"
        ```
        This will return a JSON response with the extracted criteria.
    """
    file_content, file_extension = await process_file(job_description)
    text = extract_text(file_content, file_extension)
    criteria = await extract_criteria(text)
    return {"criteria": criteria}