import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import math

import base64
from colorama import Fore
from io import BytesIO

# Define function to find standard deviation of variables
def deviation(arr, mean):
    arr = sorted(arr)
    num = 0
    for i in arr:
        num += (i - mean) ** 2

    return math.sqrt(num / len(arr))

def find_correlation(finaldata: pd.DataFrame, columnA, columnB, mean_A, mean_B):
    covariance = np.sum((finaldata[columnA] - mean_A) * (finaldata[columnB] - mean_B)) / len(finaldata)
    correlation = covariance / (deviation(finaldata[columnA],mean_A) * deviation(finaldata[columnB],mean_B))
    return round(correlation, 2), round(covariance, 2)

def get_heat_map_correlation_and_engagement_metrics(finaldata:pd.DataFrame)->str:
    print(f"{Fore.YELLOW}SUB-PROCESS: Getting heatmap..." + Fore.RESET)

    fig = plt.figure(figsize=(10, 8))
    corr = finaldata[['Views', 'Likes', 'Comments', 'Saves', 'Shares', 'Duration(sec)']].corr()
    sns.heatmap(corr, annot=True, cmap='YlGnBu')
    plt.title('Correlation between Views and Engagement Metrics',fontweight='bold')

    # Convert plot to HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Return HTML containing the plot
    return f"data:image/png;base64,{plot_data}"