from openai import OpenAI


client = OpenAI()

def extract_criteria(job_description: str) -> list:
    prompt = f"""
    Extract the key ranking criteria for hiring from the following job description:
    {job_description}
    Return the response in JSON format with keys: 'criteria' (list of key ranking factors).
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI assistant that extracts ranking criteria from job descriptions."},
                  {"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message['content']
