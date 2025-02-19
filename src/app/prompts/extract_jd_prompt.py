JD_PROMPT ="""
    **Instructions:**
    - Extract all relevant details from the job description and map them to the corresponding fields in the schema.
    - For any field not mentioned or applicable in the job description remove from output.
    - Do not include any extra keys or commentary. Output should be valid JSON only.
    
    **Job Description:**
    {job_description}
    
    Provide only the JSON output.
    """