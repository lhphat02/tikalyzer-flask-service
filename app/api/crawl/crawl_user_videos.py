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
from ...service.crawl_user_videos import crawl_user_videos
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
    await crawl_user_videos(user_name)
    response = Response()
    result_data = response.get_response()

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
