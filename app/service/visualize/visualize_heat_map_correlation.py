import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

import base64
from io import BytesIO

def get_heat_map_correlation_and_engagement_metrics(finaldata:pd.DataFrame)->str:
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