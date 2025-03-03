from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Union, Literal

class ComparisonOperator(Enum):
    LESS_THAN = "<"
    GREATER_THAN = ">"
    EQUAL_TO = "=="
    LESSER_OR_EQUAL_TO = "<="
    GREATER_OR_EQUAL_TO = ">="


class SortOperation(BaseModel):
    type: Literal["sort"]
    column: str = Field(description="Column name to sort the DataFrame by")
    ascending: bool = Field(description="Sort direction - True for ascending order (low to high), False for descending order (high to low)")

class FilterOperation(BaseModel):
    type: Literal["filter"]
    column: str = Field(description="Column name to apply the filter condition on") 
    operator: ComparisonOperator = Field(description="Comparison operator (<, >, ==, <=, >=) for the filter condition")
    value: int = Field(description="Value to compare column entries against")

class Operation(BaseModel):
    action: Union[SortOperation, FilterOperation] = Field(description="The sort or filter operation to perform")

class DataFrameTransformation(BaseModel):
    operations: List[Operation] = Field(description="Sequence of sort and filter operations to transform the DataFrame")
    limit: int = Field(description="Maximum number of rows to return in the result")