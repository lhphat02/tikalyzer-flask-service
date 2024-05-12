import pandas as pd
import matplotlib.pyplot as plt

import base64
from colorama import Fore
from io import BytesIO


def get_top_size_pie_chart(df:pd.DataFrame)->str:
    print(f"{Fore.YELLOW}SUB-PROCESS: Getting top size pia chart..." + Fore.RESET)

    top_100_views = df.sort_values(by='Views',ascending=False).head(100)

    view_count_by_video_size = top_100_views.groupby(['Video Height','Video Width'],as_index=False).size()
    view_count_by_video_size.rename(columns={'size': 'Number of videos'},inplace=True)
    view_count_by_video_size = view_count_by_video_size.sort_values(by='Number of videos',ascending=False).reset_index()

    pie_df = pd.DataFrame(columns=['Video Size','Number of videos'])
    for i in range(0,4):
        pie_df.loc[i] = {'Video Size': f"({view_count_by_video_size.loc[i, 'Video Height']}, {view_count_by_video_size.loc[i, 'Video Width']})",
                   'Number of videos': view_count_by_video_size.loc[i, 'Number of videos']}
        pie_df.loc[len(pie_df)] = {'Video Size': "Other", 'Number of videos': view_count_by_video_size['Number of videos'][4:].sum()}

    plt.figure(figsize=(10, 10))
    colors = ['mistyrose','mintcream','lightyellow','papayawhip','lavender']
    plt.pie(pie_df['Number of videos'], labels=pie_df['Video Size'], startangle=270, autopct='%1.0f%%', colors=colors)
    plt.title('Pie Chart with Top 4 Rows and Other')

    # Convert plot to HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Return HTML containing the plot
    return f"data:image/png;base64,{plot_data}"