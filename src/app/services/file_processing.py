from fastapi import UploadFile, HTTPException
import pandas as pd
from io import StringIO

# Define allowed file types and maximum file size (e.g., 5 MB)
ALLOWED_FILE_TYPES = {"pdf", "docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

async def process_file(file: UploadFile) -> tuple[bytes, str]:
    """
    Processes an uploaded file, validates its type and size, and returns the file content and extension.

    Args:
        file (UploadFile): The uploaded file.

    Returns:
        tuple[bytes, str]: A tuple containing the file content and file extension.

    Raises:
        HTTPException: If the file type is not allowed or the file size exceeds the limit.
    """
    # Validate file type
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types are: {', '.join(ALLOWED_FILE_TYPES)}",
        )

    # Validate file size
    file_size = file.size
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds the maximum limit of {MAX_FILE_SIZE / (1024 * 1024)} MB",
        )

    # Read file content
    file_content = await file.read()

    return file_content, file_extension

async def process_csv_file(file: UploadFile) -> pd.DataFrame:

    try:
        # Read file contents into memory
        contents = await file.read()

        # Convert bytes to string
        csv_string = contents.decode("utf-8")

        # Load into a Pandas DataFrame
        df = pd.read_csv(StringIO(csv_string))
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
    
    except Exception as e:
        return {"error": str(e)}