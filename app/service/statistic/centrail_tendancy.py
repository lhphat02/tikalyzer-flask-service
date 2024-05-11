import pandas as pd
import statistics

def get_median(df: pd.DataFrame, attribute: str):
    """
    Get the median of the specified attribute in the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        attribute (str): Attribute for which to calculate the median.

    Returns:
        float: Median of the specified attribute.
    """
    # Calculate the median of the specified attribute
    median = statistics.median(df[attribute])

    return median

def get_mean(df: pd.DataFrame, attribute: str):
    """
    Get the mean of the specified attribute in the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        attribute (str): Attribute for which to calculate the mean.

    Returns:
        float: Mean of the specified attribute.
    """
    # Calculate the mean of the specified attribute
    mean = statistics.mean(df[attribute])

    return mean

def get_mode(df: pd.DataFrame, attribute: str):
    """
    Get the mode of the specified attribute in the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        attribute (str): Attribute for which to calculate the mode.

    Returns:
        float: Mode of the specified attribute.
    """
    # Calculate the mode of the specified attribute
    mode = statistics.mode(df[attribute])

    return mode