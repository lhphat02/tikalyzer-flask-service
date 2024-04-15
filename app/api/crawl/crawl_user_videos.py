import aiofiles
import asyncio
import time
import os

from colorama import Fore
from datetime import datetime
from flask import Blueprint, jsonify, request
from TikTokApi import TikTokApi

from ...model.response import Response
from ...model.crawl_response_data import CrawlResponseData
from . import ms_token

crawl_user_videos_bp = Blueprint('crawl_user_videos', __name__)

async def get_user_videos(user_name):
    """
    Get user videos data and save it to a CSV file in 'csv' folder.
    
    Args:
        user_name (str): TikTok user name.
        
    Returns:
        dict["success"] (bool): True if the user videos data has been saved to a CSV file, False otherwise.
        dict["message"] (str): Response message.
        dict["data"] (object): Response data.
    """

    path_name = "csv/user/"
    start_time = time.time()
    row_count = 0
    response = Response()
    result_data = response.get_response()

    async with TikTokApi() as api:
        # Create TikTok sessions
        await api.create_sessions(headless=True, ms_tokens=[ms_token], num_sessions=1, sleep_after=1,executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe")

        # Get user videos count
        user = api.user(user_name)
        user_data = await user.info()
        post_count = user_data["userInfo"]["stats"].get("videoCount")
        data_count = 1000 if post_count > 300 else post_count

        # Check if user folder available
        if not os.path.exists(path_name):
            os.makedirs(path_name)

        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")[0:10].replace("-", "")

        # Save user videos data to a CSV file
        async with aiofiles.open(f"{path_name}user_videos_{user_name}_{current_date}.csv", "w", encoding='utf-8') as f:

            # Write header labels for the CSV file
            header_labels = "Create_time,Create_year,Create_month,Create_day,Create_hour,Likes,Comments,Saves,Views,Shares,Duration(sec),Video Height,Video Width\n"
            await f.write(header_labels)

            try:
                async for video in user.videos(count=data_count):
                    # Initialize video data
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

                    # Write video data to the CSV file
                    row = f'{video_data["Create_time"]},"{video_data["Create_year"]}","{video_data["Create_month"]}","{video_data["Create_day"]}","{video_data["Create_hour"]}","{video_data["Likes"]}","{video_data["Comments"]}",{video_data["Saves"]},{video_data["Views"]},{video_data["Shares"]},{video_data["Duration(sec)"]},{video_data["Video Height"]},{video_data["Video Width"]}\n'
                    await f.write(row)

                    # Increment row count
                    row_count += 1

            except Exception as e:
                # Set response data
                response.set_response(False, e)
                print("\n" + Fore.RED + f"Error: {e}" + Fore.RESET)
                return result_data

            finally:
                # Close the file
                await f.close()
        
    # Calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Create response data
    response_data = CrawlResponseData(file = f"user_videos_{user_name}_{current_date}.csv", path = path_name, elapsed_time = elapsed_time, row_count = row_count)

    # Set response data
    response.set_response(True, f"{row_count} user videos data has been saved to a CSV file.", response_data)

    print("\n" + Fore.GREEN + result_data["message"] + Fore.RESET)
    return result_data

@crawl_user_videos_bp.route('/crawl-user-videos')
def crawl_user_videos():
    # Get user name from the request parameters
    user_name = request.args.get('user_name')
    if not user_name:
        return jsonify({"error": "user_name parameter is missing."}), 400

    # Get user videos data
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    user_videos_data = loop.run_until_complete(get_user_videos(user_name))
    return jsonify(user_videos_data)
