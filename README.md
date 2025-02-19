# Hiring Helper

**Description:**  
Hiring Helper is a FastAPI application that helps HR professionals extract job criteria from job descriptions, score candidate resumes, and generate reports in CSV format.

---

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [License](#license)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Kayalvizhi42/hiring_helper.git
   cd hiring_helper
   ```

2. **Install dependencies:**

    This is a `uv` project. Install `uv`

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh

   ```
   and create the virtual environment for the project using

    ```bash
    uv sync
    ```

    activate virtual environment using 
    ```bash
    source .venv/bin/activate
    ```


---

## Configuration

- **.env**:  
  This file contains configuration parameters for the project.  Rename the `.env.example` file to `.env`

  to enable the `src` directory to be accessed as a python package set the path to the src folder. 

  ```bash
    PYTHONPATH=current-working-directory/src
    OPENAI_API_KEY=your-key-here
  ```

---


## Project Structure
### Explanation of Key Components

- **API Endpoints:**  
  - **`extract_criteria.py`**: Contains the endpoint to extract ranking criteria from job descriptions.  
  - **`score_resumes.py`**: Contains the endpoint to score candidate resumes against the provided criteria.  
  - **`score_resumes_json.py`**: Returns the scores in a structured json format.

- **Models:**  
  - **Job Requirements Models:** Define the schema for job description criteria.  
  - **Resume Score Models:** Define the schema for scoring candidate resumes.

- **Prompts:**  
  - **`extract_jd_prompt.py` and `score_resume_prompt.py`**: Contain the prompt templates used for interacting with the language models (LLMs) to extract criteria and score resumes.

- **Services:**  
  - **File Processing:** Handles processing uploaded files (PDFs, DOCXs, etc.).  
  - **Text Extraction:** Extracts text content from job descriptions and resumes.  
  - **Scoring:** Implements the logic for evaluating candidate resumes against the job criteria.  
  - **Format Table:** Contains utility functions to flatten JSON objects into tables for CSV export.

- **Samples:**  
  Provides sample criteria, job descriptions, resumes, and output files to help test and demonstrate the application's functionality.

- **Tests:**  
  Contains automated tests to ensure each endpoint works as expected (e.g., testing CSV downloads, criteria extraction, and resume scoring).

---

## Usage

1. **Running the Application:**

    With the virtual environment active, run the service using

    ```bash
    fastapi run src/app/main.py
    ```
    Open `http://0.0.0.0:8000/docs` to access the swagger ui

2. **Accessing Endpoints:**

   - **Extract Criteria:** `POST /extract-criteria`  
     

   - **Score Resumes:** `POST /score-resumes`  
     


---

## Testing

To run the automated tests:

```bash
pytest src/tests
```

---

## License

[Fill in the license information or reference the LICENSE file.]

---

## Contributing

[Describe how contributors can get involved.]

---

## Acknowledgments

[Credit any resources, libraries, or inspirations.]

---


