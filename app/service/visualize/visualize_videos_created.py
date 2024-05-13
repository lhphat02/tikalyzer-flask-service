import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

import base64
from io import BytesIO
from colorama import Fore

def videos_created_by_year(data):
    """
    Count the number of videos created each year.

    Args:
        data (list): A list of years representing the creation year of each video.

    Returns:
        dict: A dictionary where the keys are the years and the values are the counts of videos created in each year.
    """
    year_counts = {}

    for row in data:
        year = row
        if year not in year_counts:
            year_counts[year] = 0
        year_counts[year] += 1

    return year_counts

def get_videos_created_by_year(df: pd.DataFrame) -> str:
    """
    Generate a bar chart showing the number of videos created by year.

    Args:
        df (pd.DataFrame): The input DataFrame containing the 'Create_year' column.

    Returns:
        str: The HTML string containing the plot as an image.

    """
    print(f"{Fore.YELLOW}SUB-PROCESS: Getting videos created by year chart..." + Fore.RESET)

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
    """
    Count the number of videos created per month.

    Args:
        data (list): A list of months representing the creation month of each video.

    Returns:
        dict: A dictionary where the keys are the months and the values are the counts of videos created in each month.
    """
    month_counts = {}

    for row in data:
        month = row
        if month not in month_counts:
            month_counts[month] = 0
        month_counts[month] += 1

    return month_counts

def get_videos_created_by_month(df: pd.DataFrame) -> str:
    """
    Generate a bar chart showing the number of videos created per month.

    Args:
        df (pd.DataFrame): The input DataFrame containing the 'Create_month' column.

    Returns:
        str: A string representing the HTML image tag containing the bar chart.
    """
    
    print(f"{Fore.YELLOW}SUB-PROCESS: Getting videos created by month chart..." + Fore.RESET)

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
    """
    Count the number of videos created per day.

    Args:
        data (list): A list of dates representing the days on which videos were created.

    Returns:
        dict: A dictionary where the keys are the days and the values are the counts of videos created on each day.
    """
    day_counts = {}

    for row in data:
        day = row
        if day not in day_counts:
            day_counts[day] = 0
        day_counts[day] += 1

    return day_counts

def get_videos_created_by_day(df: pd.DataFrame) -> str:
    """
    Generate a bar chart showing the number of videos created per day.

    Args:
        df (pd.DataFrame): The input DataFrame containing the 'Create_day' column.

    Returns:
        str: A string representing the HTML image tag containing the bar chart.
    """
    print(f"{Fore.YELLOW}SUB-PROCESS: Getting videos created by day chart..." + Fore.RESET)

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


def videos_created_by_time_period(data):
    """
    Counts the number of videos created in each time period.

    Args:
        data (list): A list of time periods.

    Returns:
        dict: A dictionary where the keys are time periods and the values are the counts of videos created in each period.
    """
    counts = {}

    for row in data:
        period = row
        if period not in counts:
            counts[period] = 0
        counts[period] += 1

    return counts

def get_videos_created_by_time_period(df: pd.DataFrame, time_period: str, color: str) -> str:
    """
    Generate a bar chart showing the number of videos created by a given time period.

    Args:
        df (pd.DataFrame): The DataFrame containing the video data.
        time_period (str): The time period to group the videos by.
        color (str): The color of the bars in the bar chart.

    Returns:
        str: The HTML string containing the plot as an image.

    """
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