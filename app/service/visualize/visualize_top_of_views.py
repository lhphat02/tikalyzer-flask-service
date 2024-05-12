import pandas as pd
import matplotlib.pyplot as plt

import base64
from io import BytesIO
from colorama import Fore

def get_views_of_top_of_day_of_week_chart(df: pd.DataFrame) -> str:
    print(f"{Fore.YELLOW}SUB-PROCESS: Getting top day of week chart..." + Fore.RESET)

    df['Create_time'] = pd.to_datetime(df['Create_time'])

    #Add created day of week column
    df['create_date_of_week'] = df['Create_time'].dt.day_name()

    top_3_days_by_mean = (
        df.groupby('create_date_of_week')['Views'].mean()
        .sort_values(ascending=False)
        .index[:3]
    )

    # Filter data to those top 3 days
    filtered_data = df[df['create_date_of_week'].isin(top_3_days_by_mean)]

    # Extract hour of day
    filtered_data['hour_of_day'] = pd.to_datetime(filtered_data['Create_time']).dt.hour

    # Group by day and hour, and aggregate total views
    views_by_day_hour = filtered_data.groupby(['create_date_of_week', 'hour_of_day'])['Views'].sum()

    # Find top hour(s) for each day of the week
    top_hours_by_day = {}
    for day in top_3_days_by_mean:
        day_data = views_by_day_hour.loc[day]
        top_hour = day_data.idxmax()
        top_views = day_data.max()

        if len(day_data) > 1 and day_data.max() == day_data.iloc[-1]:
            top_hours_by_day[day] = (top_hour, top_views, "and last hour")
        else:
            top_hours_by_day[day] = (top_hour, top_views)

    data = []
    for day, values in top_hours_by_day.items():
        hour, views = values[:2]
        data.append({'Day of Week': day, 'Hour of Day': hour, 'Views': views})

    new_df = pd.DataFrame(data)

    plt.figure(figsize=(10, 6))
    plt.bar(new_df['Day of Week'], new_df['Views'], color='teal')
    plt.xlabel('Day of Week')
    plt.ylabel('Number of Views')
    plt.xticks(rotation=45, ha='right')

    # Convert plot to HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Return HTML containing the plot
    return f"data:image/png;base64,{plot_data}"