from openai import AsyncOpenAI
from app.prompts.extract_jd_prompt import JD_PROMPT
from app.prompts.score_resume_prompt import SR_PROMPT
from app.prompts.query_filter_prompt import FILTER_PROMPT, example
from app.models.job_requirements_model import JobRequirements
from app.models.resume_score_model import JobMatchScore
from app.models.dataframe_transformation_model import DataFrameTransformation


client = AsyncOpenAI()

async def extract_criteria(job_description: str) -> JobRequirements | None:
    prompt = JD_PROMPT.format(job_description=job_description)
    
    response = await client.beta.chat.completions.parse(
        model="o3-mini",
        messages=[{"role": "system", "content": "You are an expert in extracting detailed job requirements from job descriptions."},
                  {"role": "user", "content": prompt}],
        response_format=JobRequirements


    )
    return response.choices[0].message.parsed

async def score_resume(criteria: dict, resume: str) -> JobMatchScore | None:
    prompt = SR_PROMPT.format(job_description=criteria, resume=resume)
    
    response = await client.beta.chat.completions.parse(
        model="o3-mini",
        messages=[{"role": "system", "content": "You are an expert job matching assistant."},
                  {"role": "user", "content": prompt}],
        response_format=JobMatchScore


    )
    return response.choices[0].message.parsed

async def generate_query_filter(columns: list, user_query: str) -> DataFrameTransformation:
    prompt = FILTER_PROMPT.format(columns=columns, query=user_query, example=example)
    
    response = await client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "You are an expert at interpreting natural language queries into structured filters."},
            {"role": "user", "content": prompt}
        ],
        response_format=DataFrameTransformation
    )
    
    return response.choices[0].message.parsed