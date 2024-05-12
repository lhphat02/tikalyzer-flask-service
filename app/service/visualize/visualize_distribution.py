import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from colorama import Fore

import base64
from io import BytesIO

def configure_matplotlib():
    """
    Configure Matplotlib to use a non-GUI backend.
    """
    matplotlib.use('agg')

configure_matplotlib() 

def get_dis_chart(df: pd.DataFrame,  column: str, color: str = "#00607A") -> str:
    """
    Create a distribution plot from the given DataFrame and return it as HTML.

    Args:
        df (DataFrame): Input DataFrame.
        column (str): Column name to plot.
        color (str): Plot color.

    Returns:
        str: HTML containing the distribution plot.
    """

    print(f"{Fore.YELLOW}SUB-PROCESS: Getting distribution chart..." + Fore.RESET)

    # Create a bar plot
    sns.displot(df[column], kde=False, color=color, bins=30, ec="black")
    plt.ylabel("Number of videos")

    # Convert plot to HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Return HTML containing the plot
    return f"data:image/png;base64,{plot_data}"