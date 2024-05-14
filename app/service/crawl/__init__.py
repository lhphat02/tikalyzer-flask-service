import os
import datetime

ms_token = os.environ.get("ms_token", None)

chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

def format_data(video: dict) -> dict:
  """
  Format video data, including a new attribute for the time interval
  between create date and current date.

  Args:
      video (dict): Video data.

  Returns:
      dict: Formatted video data with a new attribute 'Time_interval'.
  """

  create_time = video.create_time.strftime("%Y-%m-%d %H:%M:%S")
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
      "Create_time": create_time,
      "Create_year": create_year,
      "Create_month": create_month,
      "Create_day": create_day,
      "Create_hour": create_hour,
      "Likes": video.stats["diggCount"],
      "Comments": video.stats["commentCount"],
      "Saves": video.stats["collectCount"],
      "Views": video.stats["playCount"],
      "Shares": video.stats["shareCount"],
      "Duration(sec)": video.as_dict["video"]["duration"],
      "Video Height": video.as_dict["video"]["height"],
      "Video Width": video.as_dict["video"]["width"],
      "Time_interval": round(time_interval, 2)
  }

  return video_data
