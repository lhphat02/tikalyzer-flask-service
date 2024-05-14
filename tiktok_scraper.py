from TikTokApi import TikTokApi
import asyncio
import os
import datetime
from colorama import Fore
import csv

ms_token = os.environ.get("ms_token", None)
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

def format_data(video):
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


async def get_trending_videos(num_data=200):
  """
  Get trending videos data and save it as a CSV file.

  Args:
    num_data (int): Number of trending videos to retrieve.

  Returns:
    dict["success"] (bool): True if the operation is successful, False otherwise.
    dict["message"] (str): Response message.
    dict["data"] (object): Response data (list of video dictionaries).
  """

  cursor = 0
  result_data = {
    "success": False,
    "message": "",
    "data": None
  }
  video_data_list = []

  async with TikTokApi() as api:
    # Create TikTok sessions
    await api.create_sessions(headless=True, ms_tokens=[ms_token], num_sessions=1, sleep_after=1, executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe")

    try:
      while cursor <= num_data:
        async for video in api.trending.videos(count=30, cursor=cursor):
          # Initialize video data
          video_data = format_data(video)

          # Append video data to the list
          video_data_list.append(video_data)

          # Increment row count
          cursor += 1
      
      with open(f"tiktok_dataset_1000.csv", "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=video_data_list[0].keys())
        writer.writeheader()
        writer.writerows(video_data_list)

      # Create response data
      response_data = {
        "success": True,
        "message": f"{len(video_data_list)} trending videos data retrieved successfully and saved as CSV.",
      }

      print(Fore.GREEN + f"{len(video_data_list)} trending videos data retrieved successfully and saved as CSV." + Fore.RESET)

      return response_data

    except Exception as e:
      # Set response data
      result_data["message"] = str(e)
      print("\n" + Fore.RED + f"Error: {e}" + Fore.RESET)
      return result_data


async def get_user_videos(user_name):
    """
    Get user videos data and return it as JSON.
    
    Args:
        user_name (str): TikTok user name.
        
    Returns:
        success (bool): True if the operation is successful, False otherwise.
        message (str): Response message.
        data (object): Response data (list of video dictionaries and row count).
    """

    video_data_list = []

    async with TikTokApi() as api:
        # Create TikTok sessions 
        await api.create_sessions(headless=True, ms_tokens=[ms_token], num_sessions=1, sleep_after=1,executable_path=chrome_path)

        # Get user videos count
        user = api.user(user_name)
        user_data = await user.info()
        post_count = user_data["userInfo"]["stats"].get("videoCount")
        data_count = 1000 if post_count > 300 else post_count

        try:
            async for video in user.videos(count=data_count):
                # Initialize video data
                video_data = format_data(video)

                print(video_data)

                # Append video data to the list
                video_data_list.append(video_data)

            print(f"{Fore.GREEN}User videos data has been retrieved successfully." + Fore.RESET)

        except Exception as e:
            print(f"{Fore.RED}Error: {e}" + Fore.RESET)
            
if __name__ == "__main__":
    # asyncio.run(get_trending_videos())
    asyncio.run(get_user_videos("lelephomaiquee"))