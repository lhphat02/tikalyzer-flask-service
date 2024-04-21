import pandas as pd

def clean_data(df: pd.DataFrame, column: str = "Views") -> pd.DataFrame:
    """
    Clean the given DataFrame by removing duplicates, missing values, and outliers of the specified column.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Main feature column.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Drop rows with missing values
    df.dropna(inplace=True)

    # Remove zero duration videos
    df = df[df["Duration(sec)"] > 0]

    # Calculate the IQR for the "Views" column
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    # Calculate the lower and upper bounds
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Remove outliers
    df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

    return df