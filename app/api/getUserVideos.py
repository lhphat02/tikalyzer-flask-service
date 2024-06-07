import os
import json
import asyncio
from flask import Blueprint, jsonify, request
from colorama import Fore
from ..model.response import Response
from ..model.data_loader import Dataloader
from ..service.crawl.get_user_videos import get_user_videos
from ..service.clean.clean_df import clean_data
from ..service.crawl.get_user_info import get_user_info

get_user_videos_bp = Blueprint('get_user_videos', __name__)

async def fetch_user_videos(user_name):
    """
    Get user videos data and return it as JSON.
    
    Args:
        user_name (str): TikTok user name.
        
    Returns:
        dict["success"] (bool): True if the user videos data has been saved to a CSV file, False otherwise.
        dict["message"] (str): Response message.
        dict["data"] (object): Response data.
    """

    response = Response()

    try:
        # Get user information
        print(f"{Fore.GREEN}PROCESS: Getting user information..." + Fore.RESET)
        user_info = await get_user_info(user_name)
        print(user_info)

        if not user_info["success"]:
            raise Exception(user_info["message"])

        video_count = user_info["data"]["userInfo"]["stats"]["videoCount"]

        # Scrape user videos data
        print(f"{Fore.GREEN}PROCESS: Scraping user videos data..." + Fore.RESET)
        user_video_data = await get_user_videos(user_name, video_count)
        
        if not user_video_data["success"]:
            raise Exception(user_video_data["message"])

        data_loader = Dataloader(user_video_data["data"]["videos"])

        # Get dataframe
        print(f"{Fore.GREEN}PROCESS: Getting user videos data as a dataframe..." + Fore.RESET)
        df = data_loader.get_df()

        # Clean user videos data
        cleaned_data = clean_data(df)

        # Final data
        final_data = cleaned_data.to_dict(orient='records')

        # Set response data
        response.success = True
        response.message = "User videos data has been generated successfully."
        response.data = {
            "videos": final_data,
            "row_count": len(final_data)
        }

        print(f"{Fore.GREEN}User videos data has been generated successfully." + Fore.RESET)

        return response.to_dict()
    
    except Exception as e:
        # Set response data
        response.message = str(e)
        response.data = []

        print(f"{Fore.RED}Error: {e}")

        return response.to_dict()
    

@get_user_videos_bp.route('/userVideos')
def user_videos():
    # Get user name from the request parameters
    user_name = request.args.get('user_name')
    if not user_name:
        return jsonify({"error": "user_name parameter is missing."}), 400

    # Get user videos data
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    user_videos_data = loop.run_until_complete(fetch_user_videos(user_name))
    return jsonify(user_videos_data)
