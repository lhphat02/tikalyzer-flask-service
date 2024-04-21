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

ms_token = 'mNjVmBJ8y1xPClasoANjANKNwSjpC5tQl8eLwdYb8mhrO75-iRsRTaOIsJfYP8eT-6Dk5jeYneZ45_6iP-jci7KNdmOnL4lpepbdHRg3f7DbexiTwPYNX9Ci92Q1kKbZAUWVvmHzqK9PdCtrFw=='

crawl_trending_videos_bp = Blueprint('crawl_trending_videos', __name__)

async def get_trending_videos(num_data=100):
    """
    Get trending videos data and save it to a CSV file in 'csv/trending' folder.

    Args:
        num_data (int): Number of trending videos to retrieve.

    Returns:
        dict["success"] (bool): True if the trending videos data has been saved to a CSV file, False otherwise.
        dict["message"] (str): Response message.
        dict["data"] (object): Response data.
    """

    path_name = "csv/trending/"
    cursor = 0
    start_time = time.time()
    row_count = 0
    response = Response()
    result_data = response.get_response()

    async with TikTokApi() as api:
        # Create TikTok sessions
        await api.create_sessions(headless=True, ms_tokens=[ms_token], num_sessions=1, sleep_after=1, executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe")

        # Check if trending folder available
        if not os.path.exists(path_name):
            os.makedirs(path_name)

        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")[0:10].replace("-", "")

        # Save trending videos data to a CSV file
        async with aiofiles.open(f"{path_name}trending_videos_{num_data}_{current_date}.csv", "w", encoding='utf-8') as f:

            # Write header labels for the CSV file
            header_labels = "Create_time,Create_year,Create_month,Create_day,Create_hour,Likes,Comments,Saves,Views,Shares,Duration(sec),Video Height,Video Width\n"
            await f.write(header_labels)

            try:
                while cursor <= num_data:
                    async for video in api.trending.videos(count=30, cursor=cursor):
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
                    
                    # Increment cursor
                    cursor += 30

            except Exception as e:
                # Set response data
                response.set_response(False, e)
                print("\n" + Fore.RED + f"Error: {e}" + Fore.RESET)
                return result_data

            finally:
                # Close the CSV file
                await f.close()

    # Calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Create response data
    response_data = CrawlResponseData(file = f"trending_videos_{num_data}_{current_date}.csv", path = path_name, elapsed_time = elapsed_time, row_count = row_count)

    # Set response data
    response.set_response(True, f"{row_count} trending videos data has been saved to a CSV file.", response_data)
    print("\n" + Fore.GREEN + result_data["message"] + Fore.RESET)
    
    return result_data

@crawl_trending_videos_bp.route('/crawl-trending-videos')
def crawl_trending_videos():
    # Get number of trending videos from the request parameters
    num_data = request.args.get('num_data', default=100, type=int)

    # Get trending videos data
    trending_videos_data = asyncio.run(get_trending_videos(num_data))
    return jsonify(trending_videos_data)
