import io
import csv
from fastapi.responses import StreamingResponse
from app.models.resume_score_model import JobMatchScore

def flatten_job_match_score(job_match_score: JobMatchScore) -> dict:
    """
    Flattens a single JobMatchScore JSON object into a dictionary with simple values.
    
    For list fields (technical_skills_match, soft_skills_match, experience_match, education_match, 
    tools_and_technology_match, strengths, and gaps), we join the list into a semicolon-delimited string.
    """
    job_match_score = job_match_score.model_dump()
    flattened = {}
    
    # Flatten list fields of SkillMatch objects
    for key in ["technical_skills_match", "soft_skills_match", "experience_match", "education_match", "tools_and_technology_match"]:
        items = job_match_score.get(key, [])
        # Format each SkillMatch as "skill_description (score)"
        for item in items:
            column_name = f"{item.get('skill_description', '').replace('_' , ' ').replace(',', '.')}"
            value = item.get('score', '')
            if type(value) is str:
                value.replace(',', '.')
            flattened[column_name] = value
    
    # Flatten integer fields directly
    flattened["location_match"] = job_match_score.get("location_match", None)
    flattened["industry_match"] = job_match_score.get("industry_match", None)
    
    # Flatten strengths and gaps lists by joining them with semicolons
    flattened["strengths"] = "; ".join([s.strip() for s in job_match_score.get("strengths", [])])
    flattened["gaps"] = "; ".join([g.strip() for g in job_match_score.get("gaps", [])])
    
    return flattened

def format_as_csv(items):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames= items[0].keys())
    writer.writeheader()
    writer.writerows(items)

    output.seek(0)
    headers = {
        "Content-Disposition": "attachment; filename=job_match_score.csv"
    }
    return StreamingResponse(output, media_type="text/csv", headers=headers)
