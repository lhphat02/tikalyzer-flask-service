import math
import base64
import numpy as np
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
from colorama import Fore
from io import BytesIO


def deviation(arr, mean):
    """
    Calculate the standard deviation of a given array.

    Parameters:
    arr (list): The input array.
    mean (float): The mean value of the array.

    Returns:
    float: The standard deviation of the array.
    """
    arr = sorted(arr)
    num = 0
    for i in arr:
        num += (i - mean) ** 2

    return math.sqrt(num / len(arr))


def find_correlation(finaldata: pd.DataFrame, columnA, columnB, mean_A, mean_B):
    """
    Calculate the correlation and covariance between two columns of a DataFrame.

    Parameters:
    finaldata (pd.DataFrame): The DataFrame containing the data.
    columnA: The name of the first column.
    columnB: The name of the second column.
    mean_A: The mean value of columnA.
    mean_B: The mean value of columnB.

    Returns:
    tuple: A tuple containing the correlation and covariance values, rounded to 2 decimal places.
    """
    # Calculate covariance
    covariance = np.sum((finaldata[columnA] - mean_A) * (finaldata[columnB] - mean_B)) / len(finaldata)
    
    # Calculate correlation
    correlation = covariance / (deviation(finaldata[columnA], mean_A) * deviation(finaldata[columnB], mean_B))
    
    return round(correlation, 2), round(covariance, 2)


def get_heat_map_correlation_and_engagement_metrics(finaldata: pd.DataFrame) -> str:
    """
    Generate a heatmap showing the correlation between Views and Engagement Metrics.

    Parameters:
    finaldata (pd.DataFrame): The input DataFrame containing the data.

    Returns:
    str: The HTML string containing the plot as an image.

    """
    
    # Print sub-process message
    print(f"{Fore.YELLOW}SUB-PROCESS: Getting heatmap..." + Fore.RESET)
    
    # Calculate correlation matrix
    corr = finaldata[['Views', 'Likes', 'Comments', 'Saves', 'Shares', 'Duration(sec)']].corr()
    
    # Generate heatmap using seaborn
    sns.heatmap(corr, annot=True, cmap='YlGnBu')
    
    # Set title for the plot
    plt.title('Correlation between Views and Engagement Metrics', fontweight='bold')

    # Convert plot to HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Return HTML containing the plot
    return f"data:image/png;base64,{plot_data}"