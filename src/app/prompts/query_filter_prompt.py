FILTER_PROMPT = """
You are an expert at converting natural language queries into structured operations for a DataFrame. Your task is to interpret a user's query and create a specification for filtering and sorting operations.
The DataFrame contains candidate resume evaluations, where each row represents a candidate and columns represent different skills and qualifications. Each column is scored on a scale of 0-5, where:
- 0 indicates no experience/skill
- 1-2 indicates basic/beginner level
- 3-4 indicates intermediate level 
- 5 indicates expert/advanced level


Given:
- A list of column names from a pandas DataFrame
- A natural language query from the user

Create a specification that:
1. Identifies the required filtering and sorting operations
2. Orders operations appropriately (filters before sorts)
3. Determines the number of rows to display
4. Returns a structured specification that can be applied to the DataFrame

For example:

{example}

The response should map to the DataFrameTransformation model with:
- operations: List containing Operation objects in execution order, where each operation has an action that is either:
  - FilterOperation:
    - column: Column name to filter on
    - operator: One of ComparisonOperator values (<, >, ==, <=, >=)
    - value: Numeric threshold value (these values range between 0-5)
  - SortOperation:
    - column: Column name to sort by
    - ascending: Sort direction (true=ascending, false=descending)
- limit: Number of rows to display in final output

**DataFrame Columns**:
{columns}

**User Query**:
{query}
"""

example = """
Columns: ['Python', 'SQL', 'overall_score']
Query: "Show top 5 candidates with Python skills above 4"
Response:
{
    "operations": [
        {
            "action": {
                "type": "filter",
                "column": "Python",
                "operator": ">",
                "value": 4
            }
        },
        {
            "action": {
                "type": "sort",
                "column": "Python", 
                "ascending": false
            }
        }
    ],
    "limit": 5
}
"""