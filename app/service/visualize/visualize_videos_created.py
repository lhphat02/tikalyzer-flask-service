import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

import base64
from io import BytesIO

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

    plt.figure(figsize=(6, 6))
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