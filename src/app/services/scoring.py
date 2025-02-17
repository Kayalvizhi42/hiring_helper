from openai import OpenAI
from app.prompts.extract_jd import JD_PROMPT
from app.prompts.score_resume import SR_PROMPT
from app.models.ranking_criteria import JobRequirements
from app.models.resume import JobMatchScore
from typing import Dict

client = OpenAI()

def extract_criteria(job_description: str) -> dict:
    prompt = JD_PROMPT.format(job_description=job_description)
    
    response = client.beta.chat.completions.parse(
        model="o1",
        messages=[{"role": "system", "content": "You are an expert in extracting detailed job requirements from job descriptions."},
                  {"role": "user", "content": prompt}],
        response_format=JobRequirements


    )
    return response.choices[0].message.parsed

def score_resume(criteria: Dict, resume: str) -> dict:
    prompt = SR_PROMPT.format(job_description=criteria, resume=resume)
    
    response = client.beta.chat.completions.parse(
        model="o1",
        messages=[{"role": "system", "content": "You are an expert job matching assistant."},
                  {"role": "user", "content": prompt}],
        response_format=JobMatchScore


    )
    return response.choices[0].message.parsed