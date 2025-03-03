from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.services.file_processing import process_csv_file
from app.services.scoring import generate_query_filter
from app.utils.transform_dataframe import apply_transformations
from app.utils.format_table import format_df_as_csv
import pandas as pd

router = APIRouter()

@router.post("/filter-resumes", response_class=FileResponse)
async def filter_resumes(
    user_query: str,
    resume_scores: UploadFile = File(...),
    ):
    df: pd.DataFrame = await process_csv_file(resume_scores)

    # upsert to qdrant doc=row, payload = candidate name

    query_filter = await generate_query_filter(df.columns.to_list(), user_query)

    df = apply_transformations(df, query_filter)

    # get candidate names

    # get qdrant db points that can be got with scroll

    # initialize a reranker, rerank the points by comparing the query and doc

    return format_df_as_csv(df)



    

