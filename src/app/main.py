from fastapi import FastAPI
from app.api.endpoints import extract_criteria, score_resumes

app = FastAPI()

app.include_router(extract_criteria.router)
app.include_router(score_resumes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Resume Ranking API"}