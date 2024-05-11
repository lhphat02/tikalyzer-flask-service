from TikTokApi import TikTokApi
import asyncio
import json
import time
import os
import datetime
from colorama import Fore

ms_token = os.environ.get("ms_token", None)

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

async def get_hashtag_videos(hash_tag, num_data=300):
    cursor = 0

    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=True, executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe")
        tag = api.hashtag(name=hash_tag)

        with open(f"csv/hashtag_{hash_tag}_{num_data}.csv" , "w", encoding='utf-8') as f:
            header_labels = "Create_time,Create_year,Create_month,Create_day,Create_hour,Likes,Comments,Saves,Views,Shares,Duration(sec),Video Height,Video Width\n"
            f.write(header_labels)

            while cursor <= num_data:
                async for video in tag.videos(count=30, cursor=cursor):
                    create_time = str(video.create_time)
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
                    row = f'{video_data["Create_time"]},"{video_data["Create_year"]}","{video_data["Create_month"]}","{video_data["Create_day"]}","{video_data["Create_hour"]}","{video_data["Likes"]}","{video_data["Comments"]}",{video_data["Saves"]},{video_data["Views"]},{video_data["Shares"]},{video_data["Duration(sec)"]},{video_data["Video Height"]},{video_data["Video Width"]}\n'
                    f.write(row)
                cursor += 30

async def get_user_videos(username):
    result_data = {
        "success": False,
        "message": "",
        "data": None
    }

    video_data_list = []

    async with TikTokApi() as api:
        await api.create_sessions(headless=True, ms_tokens=[ms_token], num_sessions=1, sleep_after=3,executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe")

        user = api.user(username)
        user_data = await user.info()
        post_count = user_data["userInfo"]["stats"].get("videoCount")

        async for video in user.videos(count=post_count):
            video_data = format_data(video)
            video_data_list.append(video_data)
            url = f"https://www.tiktok.com/@{video.as_dict['author']['uniqueId']}/video/{video.id}"
            print(f"URL: {url}") 

    with open(f"test.json", "w") as json_file:
        json.dump(video_data_list, json_file, indent=4)

    result_data["success"] = True
    result_data["message"] = f"{len(video_data_list)} videos data retrieved successfully."
    result_data["data"] = video_data_list

    return result_data


    
async def get_trending_videos(num_data=10):
    """
    Get trending videos data and return it as JSON.

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
            
            with open(f"test.json", "w") as json_file:
                json.dump(video_data_list, json_file, indent=4)

            # Create response data
            response_data = {
                "success": True,
                "message": f"{len(video_data_list)} trending videos data retrieved successfully.",
                "data": video_data_list
            }

            return response_data

        except Exception as e:
            # Set response data
            result_data["message"] = str(e)
            print("\n" + Fore.RED + f"Error: {e}" + Fore.RESET)
            return result_data

            
if __name__ == "__main__":
    # asyncio.run(get_trending_videos())
    # asyncio.run(get_hashtag_videos("sofm", 150))
    # asyncio.run(get_user_videos_legacy("sofm_official", 150))
    asyncio.run(get_user_videos("sofm_official "))