# services/csv_converter.py
import pandas as pd
from io import StringIO

def convert_df_to_csv(df: pd.DataFrame) -> str:
    """
    Convert a pandas DataFrame to a CSV string.

    Args:
        df (pd.DataFrame): The DataFrame to convert.

    Returns:
        str: The CSV string.
    """
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()
