import pandas as pd
import base64
import matplotlib.pyplot as plt

from io import BytesIO
from colorama import Fore


def get_views_of_top_of_day_of_week_chart(df: pd.DataFrame) -> str:
    """
    Generate a bar plot of the top hours by day of the week based on the number of views.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data.

    Returns:
        str: The HTML string containing the plot.

    """
    
    # Print a message indicating the start of the sub-process
    print(f"{Fore.YELLOW}SUB-PROCESS: Getting top day of week chart..." + Fore.RESET)

    # Convert 'Create_time' column to datetime format
    df['Create_time'] = pd.to_datetime(df['Create_time'])

    # Add a new column 'create_date_of_week' to store the day of the week
    df['create_date_of_week'] = df['Create_time'].dt.day_name()

    # Find the top 3 days with the highest mean views
    top_3_days_by_mean = (
        df.groupby('create_date_of_week')['Views'].mean()
        .sort_values(ascending=False)
        .index[:3]
    )

    # Filter the data to include only the top 3 days
    filtered_data = df[df['create_date_of_week'].isin(top_3_days_by_mean)].copy()

    # Extract the hour of the day from 'Create_time'
    filtered_data['hour_of_day'] = pd.to_datetime(filtered_data['Create_time']).dt.hour

    # Group the data by day of the week and hour of the day, and calculate the total views
    views_by_day_hour = filtered_data.groupby(['create_date_of_week', 'hour_of_day'])['Views'].sum()

    # Find the top hour(s) for each day of the week
    top_hours_by_day = {}
    for day in top_3_days_by_mean:
        day_data = views_by_day_hour.loc[day]
        top_hour = day_data.idxmax()
        top_views = day_data.max()

        # Check if there are multiple top hours with the same views
        if len(day_data) > 1 and day_data.max() == day_data.iloc[-1]:
            top_hours_by_day[day] = (top_hour, top_views, "and last hour")
        else:
            top_hours_by_day[day] = (top_hour, top_views)

    # Create a new DataFrame to store the top hours for each day
    data = []
    for day, values in top_hours_by_day.items():
        hour, views = values[:2]
        data.append({'Day of Week': day, 'Hour of Day': hour, 'Views': views})

    new_df = pd.DataFrame(data)

    # Create a bar plot of the top hours by day of the week
    plt.figure(figsize=(10, 6))
    plt.bar(new_df['Day of Week'], new_df['Views'], color='teal')
    plt.xlabel('Day of Week')
    plt.ylabel('Number of Views')
    plt.xticks(rotation=45, ha='right')

    # Convert the plot to HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Return the HTML containing the plot
    return f"data:image/png;base64,{plot_data}"
