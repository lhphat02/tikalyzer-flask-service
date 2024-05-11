import base64
from io import BytesIO

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import statistics

def get_median_tendancy(df: pd.DataFrame, attribute: str):
    """
    Get the median of the specified attribute in the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        attribute (str): Attribute for which to calculate the median.

    Returns:
        float: Median of the specified attribute.
    """
    # Calculate the median of the specified attribute
    median = df[attribute].median()

    return median