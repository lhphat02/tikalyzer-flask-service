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

# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import matplotlib
# from colorama import Fore
# import base64
# from io import BytesIO
# import numpy as np

# def configure_matplotlib():
#     """
#     Configure Matplotlib to use a non-GUI backend.
#     """
#     matplotlib.use('agg')

# configure_matplotlib() 

# def get_dynamic_bins(df: pd.DataFrame, column: str) -> list:
#     """
#     Calculate dynamic bins based on the distribution of the data.

#     Args:
#         df (DataFrame): Input DataFrame.
#         column (str): Column name to calculate bins for.

#     Returns:
#         list: List of bin edges.
#     """
#     quantiles = df[column].quantile([0, 0.25, 0.5, 0.75, 1.0]).values
#     bins = [0, quantiles[1], quantiles[2], quantiles[3], quantiles[4]]
#     return bins

# def get_dis_chart(df: pd.DataFrame, column: str) -> str:
#     """
#     Create a pie chart showing the distribution of views as percentages of total videos.

#     Args:
#         df (DataFrame): Input DataFrame.
#         column (str): Column name to plot.

#     Returns:
#         str: HTML containing the pie chart.
#     """

#     print(f"{Fore.YELLOW}SUB-PROCESS: Getting view distribution chart..." + Fore.RESET)

#     # Calculate dynamic bins
#     bins = get_dynamic_bins(df, column)
#     labels = [f'<= {bins[1]:.1f}', f'{bins[1]:.1f} - {bins[2]:.1f}', f'{bins[2]:.1f} - {bins[3]:.1f}', f'> {bins[3]:.1f}']

#     # Categorize videos into these ranges
#     df['view_range'] = pd.cut(df[column], bins=bins, labels=labels, include_lowest=True)

#     # Calculate the percentage distribution
#     distribution = df['view_range'].value_counts(normalize=True) * 100

#     # Create a pie chart
#     plt.figure(figsize=(10, 8))  # Adjust the figure size for better fit
#     wedges, texts, autotexts = plt.pie(distribution, labels=distribution.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'),
#                                        pctdistance=0.85, labeldistance=1.1, startangle=140)

#     # Improve the label aesthetics
#     for text in texts:
#         text.set_color('grey')
#         text.set_fontsize(10)
#     for autotext in autotexts:
#         autotext.set_color('white')
#         autotext.set_fontsize(10)

#     # Add a legend
#     plt.legend(wedges, labels=distribution.index, title="Ranges", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

#     # Convert plot to HTML
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png', bbox_inches='tight')  # Use bbox_inches='tight' to avoid cropping
#     buffer.seek(0)
#     plot_data = base64.b64encode(buffer.read()).decode('utf-8')
#     plt.close()

#     # Return HTML containing the plot
#     return f"data:image/png;base64,{plot_data}"