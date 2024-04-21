import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import base64
from io import BytesIO

def get_dis_chart(df: pd.DataFrame,  column: str, ylabel: str, title: str, color: str = "blue") -> str:
    """
    Create a distribution plot from the given DataFrame and return it as HTML.

    Args:
        df (DataFrame): Input DataFrame.
        column (str): Column name to plot.
        ylabel (str): Label for the y-axis.
        title (str): Title of the plot.

    Returns:
        str: HTML containing the distribution plot.
    """

    # Create a bar plot
    sns.displot(df[column], kde=False, color=color, bins=30, ec="black")
    plt.ylabel(ylabel)
    plt.title(title)

    # Convert plot to HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Return HTML containing the plot
    return f'<img src="data:image/png;base64,{plot_data}" alt="bar chart">'