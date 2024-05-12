import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error


def get_predicted_view_count(video_url: str) -> int:
    """
    Get the predicted view count for the given video data and calculate accuracy.

    Args:
        new_video (dict): New video data.

    Returns:
        int: Predicted view count.
    """

    

    model_path = f"./ml-models/tiktok_rf_100k.pkl"
    model = joblib.load(model_path)

    # Format the new video data
    new_data = format_data(new_video, predict_day_interval)
    predicted_views = model.predict(new_data)[0]

    return int(predicted_views)


###############################################################


def format_data(new_video: dict, predict_day_interval) -> dict:
    """
    Format video data into a dictionary.

    Args:
        new_video (dict): Video data.

    Returns:
        dict: Formatted video data.
    """
    # Format the new video data
    create_time = new_video["Create_time"]
    create_year = int(create_time[0:4])
    create_month = int(create_time[5:7])
    create_day = int(create_time[8:10])
    create_hour = int(create_time[11:13])
    duration = new_video["Duration(sec)"]
    height = new_video["Video Height"]
    width = new_video["Video Width"]
    time_interval = predict_day_interval

    # Predict the view count
    new_data = pd.DataFrame({
        "Create_year": [create_year],
        "Create_month": [create_month],
        "Create_day": [create_day],
        "Create_hour": [create_hour],
        "Duration(sec)": [duration],
        "Time_interval": [time_interval],
        "Video Height": [height],
        "Video Width": [width]
    })

    return new_data


def get_video_id(video_url):
    # Split the URL by '/' and '?' to get individual components
    parts = video_url.split('/')
    if len(parts) < 6:
        return None  # Not a valid TikTok URL
    # The video ID is the fourth last component
    video_id = parts[-4]
    return video_id