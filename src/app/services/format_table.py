import json
import pandas as pd

def flatten_job_match_score(job_match_score: dict) -> dict:
    """
    Flattens a single JobMatchScore JSON object into a dictionary with simple values.
    
    For list fields (technical_skills_match, soft_skills_match, experience_match, education_match, 
    tools_and_technology_match, strengths, and gaps), we join the list into a semicolon-delimited string.
    """
    flattened = {}
    
    # Flatten list fields of SkillMatch objects
    for key in ["technical_skills_match", "soft_skills_match", "experience_match", "education_match", "tools_and_technology_match"]:
        items = job_match_score.get(key, [])
        # Format each SkillMatch as "skill_description (score)"
        
        flattened[key] = "; ".join(
            [f"{item.get('skill_description', '').strip()} ({item.get('score', '')})" for item in items]
        )
    
    # Flatten integer fields directly
    flattened["location_match"] = job_match_score.get("location_match", None)
    flattened["industry_match"] = job_match_score.get("industry_match", None)
    
    # Flatten strengths and gaps lists by joining them with semicolons
    flattened["strengths"] = "; ".join([s.strip() for s in job_match_score.get("strengths", [])])
    flattened["gaps"] = "; ".join([g.strip() for g in job_match_score.get("gaps", [])])
    
    return flattened

def main():
    # Load the JSON data from a file (adjust the file name/path as needed)
    with open("job_match_score.json", "r") as f:
        data = json.load(f)
    
    # Determine if data contains a "results" key or is a list or single object
    if isinstance(data, dict) and "results" in data:
        items = data["results"]
    elif isinstance(data, list):
        items = data
    else:
        items = [data]
    
    # Flatten each JobMatchScore object
    flattened_list = [flatten_job_match_score(item) for item in items]
    
    # Create a pandas DataFrame and export to CSV
    df = pd.DataFrame(flattened_list)
    df.to_csv("job_match_score.csv", index=False)
    print("CSV exported successfully as 'job_match_score.csv'.")

if __name__ == "__main__":
    main()
