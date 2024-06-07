from TikTokApi import TikTokApi
import joblib
import datetime
import os
import asyncio

model_path = f"./app/service/machinelearning/ml-models/tiktok_rf_100k.pkl"
ms_token = os.environ.get("ms_token", None)
executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe"

async def get_predicted_view_count(video_url: str) -> int:
    """
    Get the predicted view count for the given video data and calculate accuracy.

    Args:
        new_video (dict): New video data.

    Returns:
        int: Predicted view count.
    """

    video_data = await get_video_data(video_url)

    new_data = [list(video_data.values())]

    model = joblib.load(model_path)

    predicted_views = model.predict(new_data)[0]

    print("Predicted views: ", predicted_views)

    return int(predicted_views)


###############################################################


async def get_video_data(video_url: str) -> dict:
  async with TikTokApi() as api:
    await api.create_sessions(headless=True, ms_tokens=[ms_token], num_sessions=1, sleep_after=1, executable_path=executable_path)
    video_info = await api.video(url=video_url).info()
    video_data = format_data(video_info)
    return video_data


def format_data(video):
  """
  Format video data, including a new attribute for the time interval
  between create date and current date.

  Args:
      video (dict): Video data.

  Returns:
      dict: Formatted video data with a new attribute 'Time_interval'.
  """
  time_stamp = int(video["createTime"])

  create_time = datetime.datetime.fromtimestamp(time_stamp).strftime("%Y-%m-%d %H:%M:%S")

  # Extract date components for clarity
  create_year = int(create_time[0:4])
  create_month = int(create_time[5:7])
  create_day = int(create_time[8:10])
  create_hour = int(create_time[11:13])
  create_minute = int(create_time[14:16])
  create_second = int(create_time[17:19])

  # Get current date and time (consider UTC if necessary)
  current_time = datetime.datetime.now()

  # Calculate time difference using datetime objects
  time_delta = current_time - datetime.datetime(create_year, create_month, create_day, create_hour, create_minute, create_second)

  # Choose the desired time unit for the interval (days, hours, minutes, seconds)
  time_interval_unit = "days"

  if time_interval_unit == "days":
    time_interval = time_delta.total_seconds() / (60 * 60 * 24)
  elif time_interval_unit == "hours":
    time_interval = time_delta.total_seconds() / (60 * 60)
  elif time_interval_unit == "minutes":
    time_interval = time_delta.total_seconds() / 60
  elif time_interval_unit == "seconds":
    time_interval = time_delta.total_seconds()
  else:
    raise ValueError("Invalid time_interval_unit. Choose 'days', 'hours', 'minutes', or 'seconds'.")

  video_data = {
      "Create_year": create_year,
      "Create_month": create_month,
      "Create_day": create_day,
      "Create_hour": create_hour,
      "Likes": video["stats"]["diggCount"],
      "Comments": video["stats"]["commentCount"],
      "Saves": video["stats"]["collectCount"],
      "Shares": video["stats"]["shareCount"],
      "Duration(sec)": video["video"]["duration"],
      "Video Height": video["video"]["height"],
      "Video Width": video["video"]["width"],
      "Time_interval": round(time_interval, 2)
  }

  return video_data


if __name__ == "__main__":
    asyncio.run(get_predicted_view_count("https://www.tiktok.com/@lazadavietnam/video/7366216481861864711"))