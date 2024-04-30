import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

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

def videos_created_by_year(data):
    year_counts = {}

    for row in data:
        year = row
        if year not in year_counts:
            year_counts[year] = 0
        year_counts[year] += 1

    return year_counts

def get_videos_created_by_year(df: pd.DataFrame, years: int, videos: int, color: str) -> str:
    number_of_videos_created_by_year = videos_created_by_year(df["Create_year"])

    years = number_of_videos_created_by_year.keys()
    videos = number_of_videos_created_by_year.values()
    dict_keys= years
    list_of_strings = [str(x) for x in dict_keys]

    plt.figure(figsize=(2, 2))
    plt.bar(years, videos, color='greenyellow', edgecolor='black', tick_label=list_of_strings)

    for bar_object, count in zip(plt.bar(years, videos, color='greenyellow', edgecolor='black', tick_label=list_of_strings), videos):
        plt.text(bar_object.get_x() + bar_object.get_width() / 2, count + 0.1, count, ha='center', va='bottom')

    plt.xlabel('Year')
    plt.ylabel('Number of Videos')
    plt.title('Videos Created By Year')
    plt.grid(True)
        # Convert plot to HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Return HTML containing the plot
    return f"data:image/png;base64,{plot_data}"

def videos_created_by_month(data):
    month_counts = {}

    for row in data:
        month = row
        if month not in month_counts:
            month_counts[month] = 0
        month_counts[month] += 1

    return month_counts

def get_videos_created_by_month(df: pd.DataFrame, months: int, videos: int, color: str) -> str:

    number_of_videos_created_by_month = videos_created_by_month(df["Create_month"])

    months = number_of_videos_created_by_month.keys()
    videos = number_of_videos_created_by_month.values()
    dict_keys = months
    list_of_strings = [str(x) for x in dict_keys]
    # Plot a bar chart
    plt.figure(figsize=(6, 6))
    plt.bar(months, videos, color='pink', edgecolor='black', tick_label=list_of_strings)

    for bar_object, count in zip(plt.bar(months, videos, color='pink', edgecolor='black', tick_label=list_of_strings), videos):
        plt.text(bar_object.get_x() + bar_object.get_width() / 2, count + 0.1, count, ha='center', va='bottom')

    plt.xlabel('Month')
    plt.ylabel('Number of Videos')
    plt.title('Videos Created By Month')

    plt.grid(True)

    # Convert plot to HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Return HTML containing the plot
    return f"data:image/png;base64,{plot_data}"

def videos_created_by_day(data):
    day_counts = {}

    for row in data:
        day = row
        if day not in day_counts:
            day_counts[day] = 0
        day_counts[day] += 1

    return day_counts

def get_videos_created_by_day(df: pd.DataFrame, days: int, videos: int, color: str)->str:

    number_of_videos_created_by_day = videos_created_by_day(df["Create_day"])

    days = number_of_videos_created_by_day.keys()
    videos = number_of_videos_created_by_day.values()
    dict_keys = days
    list_of_strings = [str(x) for x in dict_keys]

    plt.figure(figsize=(10, 6))
    plt.bar(days, videos, color='blueviolet', edgecolor='black', tick_label=list_of_strings)

    for bar_object, count in zip(plt.bar(days, videos, color='blueviolet', edgecolor='black', tick_label=list_of_strings), videos):
        plt.text(bar_object.get_x() + bar_object.get_width() / 2, count + 0.1, count, ha='center', va='bottom')

    plt.xlabel('Day')
    plt.ylabel('Number of Videos')
    plt.title('Videos Created By Day')

    plt.grid(True)

    # Convert plot to HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Return HTML containing the plot
    return f"data:image/png;base64,{plot_data}"

def videos_created_by_time_period(data, time_period):
    counts = {}

    for row in data:
        period = row
        if period not in counts:
            counts[period] = 0
        counts[period] += 1

    return counts

def get_videos_created_by_time_period(df: pd.DataFrame, time_period: str, color: str) -> str:
    number_of_videos_created_by_time_period = videos_created_by_time_period(df[time_period])

    periods = number_of_videos_created_by_time_period.keys()
    videos = number_of_videos_created_by_time_period.values()
    dict_keys = periods
    list_of_strings = [str(x) for x in dict_keys]

    plt.figure(figsize=(10, 6))
    plt.bar(periods, videos, color=color, edgecolor='black', tick_label=list_of_strings)

    for bar_object, count in zip(plt.bar(periods, videos, color=color, edgecolor='black', tick_label=list_of_strings), videos):
        plt.text(bar_object.get_x() + bar_object.get_width() / 2, count + 0.1, count, ha='center', va='bottom')

    plt.xlabel(time_period.capitalize())
    plt.ylabel('Number of Videos')
    plt.title(f'Videos Created By {time_period.capitalize()}')
    plt.grid(True)

    # Convert plot to HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    # Return HTML containing the plot
    return f"data:image/png;base64,{plot_data}"

def get_top_4_rows_and_other(df:pd.DataFrame, column:str, color: str)->str:

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