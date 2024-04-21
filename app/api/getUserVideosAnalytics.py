import asyncio

from flask import Blueprint, jsonify, request
from colorama import Fore

from ..model.response import Response
from ..model.data_loader import Dataloader
from ..service.crawl.get_user_videos import get_user_videos
from ..service.clean.clean_df import clean_data
from ..service.visualize.visualize_distribution import get_dis_chart

get_user_videos_analytics_bp = Blueprint('get_user_videos_analytics', __name__)

async def get_user_videos_analytics(user_name):
    """
    Get user videos data and save it to a CSV file in 'csv' folder.
    
    Args:
        user_name (str): TikTok user name.
        
    Returns:
        dict["success"] (bool): True if the user videos data has been saved to a CSV file, False otherwise.
        dict["message"] (str): Response message.
        dict["data"] (object): Response data.
    """

    response = Response()

    try:
        # Scrape user videos data
        user_video_data = await get_user_videos(user_name)

        # Get data loader from user videos data
        data_loader = Dataloader(user_video_data["data"]["videos"])

        # Get dataframe
        df = data_loader.get_df()

        # Clean user videos data
        cleaned_data = clean_data(df)

        # Get distribution chart
        dist_chart = get_dis_chart(cleaned_data, 'Views', "Number of videos", "Views distribution")

        # Set response data
        response.success = True
        response.message = "User videos data has been retrieved successfully."
        response.data["videos"] = user_video_data["data"]["videos"]
        response.data["total"] = user_video_data["data"]["total"]
        response.data["dist_chart"] = dist_chart

        print(f"{Fore.GREEN}User videos data has been retrieved successfully.")

        return response.to_dict()
    
    except Exception as e:
        # Set response data
        response.message = e
        response.data = None

        print(f"{Fore.RED}Error: {e}")

        return response.to_dict()
    

@get_user_videos_analytics_bp.route('/userVideosAnalytics')
def user_videos_analytics():
    # Get user name from the request parameters
    user_name = request.args.get('user_name')
    if not user_name:
        return jsonify({"error": "user_name parameter is missing."}), 400

    # Get user videos data
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    user_videos_data = loop.run_until_complete(get_user_videos_analytics(user_name))
    return jsonify(user_videos_data)

