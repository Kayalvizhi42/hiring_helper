from fastapi.responses import FileResponse
from app.models.resume_score_model import JobMatchScore
import pandas as pd
from pandas import DataFrame

def flatten_job_match_score(job_match_score: JobMatchScore) -> dict:
    """
    Flattens a single JobMatchScore JSON object into a dictionary with simple values.
    
    For list fields (technical_skills_match, soft_skills_match, experience_match, education_match, 
    tools_and_technology_match, strengths, and gaps), we join the list into a semicolon-delimited string.
    """
    job_match_score_dict = job_match_score.model_dump()
    flattened = {}
    total_score = 0
    # Flatten list fields of SkillMatch objects
    for key in ["technical_skills_match", "soft_skills_match", "experience_match", "education_match", "tools_and_technology_match"]:
        items = job_match_score_dict.get(key, [])
        # Format each SkillMatch as "skill_description (score)"
        for item in items:
            column_name = f"{item.get('skill_description', '').replace('_' , ' ').replace(',', '.')}"
            value = item.get('score', '')
            if type(value) is str:
                value.replace(',', '.')
            elif type(value) is int:
                total_score += value
            flattened[column_name] = value
    
    # Flatten integer fields directly
    flattened["location_match"] = job_match_score_dict.get("location_match", None)
    flattened["industry_match"] = job_match_score_dict.get("industry_match", None)
    flattened["candidate_name"] = job_match_score.candidate_name
    
    # Flatten strengths and gaps lists by joining them with semicolons
    # flattened["strengths"] = "; ".join([s.strip() for s in job_match_score.get("strengths", [])])
    # flattened["gaps"] = "; ".join([g.strip() for g in job_match_score.get("gaps", [])])
    flattened["overall_score"] = total_score
    
    return flattened

def format_as_csv(items):
    items_df: DataFrame = pd.DataFrame(items).fillna("")
    items_df.set_index('candidate_name')
    file_path = 'samples/output/job_match_score.csv'
    items_df.to_csv(file_path)

    return FileResponse(file_path, media_type="text/csv", filename="job_match_score.csv")


def format_df_as_csv(df: pd.DataFrame):
    file_path = 'samples/output/filtered_resumes.csv'
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.to_csv(file_path)

    return FileResponse(file_path, media_type="text/csv", filename="filtered_resumes.csv")