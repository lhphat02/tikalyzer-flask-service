import base64
import pandas as pd
import matplotlib.pyplot as plt

from colorama import Fore
from io import BytesIO

def get_top_size_pie_chart(df: pd.DataFrame) -> str:
    # Print a message indicating the sub-process
    print(f"{Fore.YELLOW}SUB-PROCESS: Getting top size pie chart..." + Fore.RESET)

    # Get the top 100 views based on 'Views' column
    top_100_views = df.sort_values(by='Views', ascending=False).head(100)
    
    # Group the views count by video size (height and width)
    view_count_by_video_size = top_100_views.groupby(['Video Height', 'Video Width'], as_index=False).size()
    view_count_by_video_size.rename(columns={'size': 'Number of videos'}, inplace=True)
    view_count_by_video_size = view_count_by_video_size.sort_values(by='Number of videos', ascending=False).reset_index()

    # Create a new DataFrame for the pie chart
    pie_df = pd.DataFrame(columns=['Video Size', 'Number of videos'])

    # Determine the loop range based on the available rows (maximum 4)
    loop_range = min(len(view_count_by_video_size), 4)
    
    # Populate the pie_df DataFrame with the top 4 video sizes and their respective counts
    for i in range(loop_range):
        pie_df.loc[i] = {'Video Size': f"({view_count_by_video_size.loc[i, 'Video Height']}, {view_count_by_video_size.loc[i, 'Video Width']})",
                         'Number of videos': view_count_by_video_size.loc[i, 'Number of videos']}

    # Calculate the count of videos for the 'Other' category
    other_count = view_count_by_video_size['Number of videos'][4:].sum()
    
    # Add the 'Other' category to the pie_df DataFrame
    pie_df.loc[len(pie_df)] = {'Video Size': "Other", 'Number of videos': other_count}

    # Create the pie chart
    plt.figure(figsize=(10, 10))
    colors = ['mistyrose', 'mintcream', 'lightyellow', 'papayawhip', 'lavender']
    plt.pie(pie_df['Number of videos'], labels=pie_df['Video Size'], startangle=270, autopct='%1.0f%%', colors=colors)
    plt.title('Pie Chart with Top 4 Rows and Other')

    # Convert the plot to HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Return the HTML containing the plot
    return f"data:image/png;base64,{plot_data}"