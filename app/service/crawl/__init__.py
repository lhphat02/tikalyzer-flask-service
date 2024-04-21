import os

ms_token = os.environ.get("ms_token", None)

chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

def format_data(video):
    """
    Format video data.

    Args:
        video (dict): Video data.

    Returns:
        dict: Formatted video data.
    """

    create_time = video.create_time.strftime("%Y-%m-%d %H:%M:%S")
    video_data = {
        "Create_time": video.create_time,
        "Create_year": create_time[0:4],
        "Create_month": create_time[5:7],
        "Create_day": create_time[8:10],
        "Create_hour": create_time[11:13],
        "Likes": video.stats["diggCount"],
        "Comments": video.stats["commentCount"],
        "Saves": video.stats["collectCount"],
        "Views": video.stats["playCount"],
        "Shares": video.stats["shareCount"],
        "Duration(sec)": video.as_dict["video"]["duration"],
        "Video Height": video.as_dict["video"]["height"],
        "Video Width": video.as_dict["video"]["width"],
    }

    return video_data