import pandas as pd
import base64
import matplotlib.pyplot as plt
from io import BytesIO

def get_top_duration_chart(df: pd.DataFrame) -> str:
    """
    Generate a bar plot of the top video durations based on the number of views.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data.

    Returns:
        str: The HTML string containing the plot.
    """
    # Group by duration and calculate the total views for each duration
    top_durations_by_views = df.groupby('Duration(sec)')['Views'].sum().sort_values(ascending=False)

    # Create a bar plot of the top video durations by views
    plt.figure(figsize=(10, 6))
    top_durations_by_views.head(10).plot(kind='bar', color='skyblue')
    plt.xlabel('Duration (sec)')
    plt.ylabel('Number of Views')

    # Convert the plot to HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Return the HTML containing the plot
    return f"data:image/png;base64,{plot_data}"