from openai import OpenAI
from app.prompts.extract_jd import JD_PROMPT
from app.models.ranking_criteria import JobRequirements


client = OpenAI()

def extract_criteria(job_description: str) -> list:
    prompt = JD_PROMPT.format(job_description=job_description)
    
    response = client.beta.chat.completions.parse(
        model="o1",
        messages=[{"role": "system", "content": "You are an expert in extracting detailed job requirements from job descriptions."},
                  {"role": "user", "content": prompt}],
        response_format=JobRequirements


    )
    return response.choices[0].message.parsed
