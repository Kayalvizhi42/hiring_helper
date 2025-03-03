from fastapi import FastAPI
from app.api.endpoints import extract_criteria, score_resumes, filter_resumes, rag_resumes # test_endpoint #, score_resumes_json

app = FastAPI()

app.include_router(extract_criteria.router)
app.include_router(score_resumes.router)
app.include_router(filter_resumes.router)
app.include_router(rag_resumes.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Resume Ranking API \n Documentation at url/docs"}