from app.models.dataframe_transformation_model import DataFrameTransformation, FilterOperation, ComparisonOperator, SortOperation
import pandas as pd



def apply_transformations(df: pd.DataFrame, transformation: DataFrameTransformation) -> pd.DataFrame:
    """
    Apply a series of transformations to a DataFrame based on a DataFrameTransformation object.
    
    Args:
        df: Input DataFrame
        transformation: DataFrameTransformation object containing filter and sort operations
        
    Returns:
        Transformed DataFrame with filters and sorts applied
    """
    result = df.copy()
    
    # Apply each operation in sequence
    for operation in transformation.operations:
        if isinstance(operation.action, FilterOperation):
            # Apply filter operation
            filter_op = operation.action
            if filter_op.operator == ComparisonOperator.GREATER_THAN:
                result = result[result[filter_op.column] > filter_op.value]
            elif filter_op.operator == ComparisonOperator.LESS_THAN:
                result = result[result[filter_op.column] < filter_op.value]
            elif filter_op.operator == ComparisonOperator.EQUAL_TO:
                result = result[result[filter_op.column] == filter_op.value]
            elif filter_op.operator == ComparisonOperator.GREATER_OR_EQUAL_TO:
                result = result[result[filter_op.column] >= filter_op.value]
            elif filter_op.operator == ComparisonOperator.LESSER_OR_EQUAL_TO:
                result = result[result[filter_op.column] <= filter_op.value]
                
        elif isinstance(operation.action, SortOperation):
            # Apply sort operation
            sort_op = operation.action
            result = result.sort_values(by=sort_op.column, ascending=sort_op.ascending)
    
    # Apply row limit if specified
    if transformation.limit:
        result = result.head(transformation.limit)
        
    return result