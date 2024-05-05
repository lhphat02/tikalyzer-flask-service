import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

import base64
from io import BytesIO



def get_views_of_top_of_day_of_week_chart(df: pd.DataFrame, column: str, color: str = "#008080") -> str:
    df['Create_time'] = pd.to_datetime(df['Create_time'])

    #Add created day of week column
    df['create_date_of_week'] = df['Create_time'].dt.day_name()

    # Find top 3 days of the week with the most views
    top_3_days = (
        df.groupby('create_date_of_week')['Views'].sum()
        .sort_values(ascending=False)
        .index[:3]
    )

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

        if len(day_data) > 1 and day_data.max() == day_data.iloc[-1]:  # Handle ties at last hour
            top_hours_by_day[day] = (top_hour, top_views, "and last hour")
        else:
            top_hours_by_day[day] = (top_hour, top_views)

    data = []
    for day, values in top_hours_by_day.items():
        hour, views = values[:2]  # Extract hour and views
        data.append({'Day of Week': day, 'Hour of Day': hour, 'Views': views})

    new_df = pd.DataFrame(data)

    plt.figure(figsize=(10, 6))  # Adjust figure size as needed
    # plt.bar(new_df[column], new_df['Views'], color=color)
    plt.bar(new_df['Day of Week'], new_df['Views'], color='teal')
    plt.xlabel('Day of Week')
    plt.ylabel('Number of Views')
    # plt.title('Views for Top Hours of Top Days of Week')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability

    # Convert plot to HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Return HTML containing the plot
    return f"data:image/png;base64,{plot_data}"