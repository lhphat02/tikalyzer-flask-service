import asyncio

from flask import Blueprint, jsonify, request
from colorama import Fore

from ..model.response import Response
from ..model.data_loader import Dataloader
from ..service.crawl.get_user_videos import get_user_videos
from ..service.crawl.get_trending_videos import get_trending_videos
from ..service.clean.clean_df import clean_data
from ..service.visualize.visualize_distribution import get_dis_chart
from ..service.visualize.visualize_heat_map_correlation import get_heat_map_correlation_and_engagement_metrics
from ..service.visualize.visualize_top_4 import get_top_4_rows_and_other
from ..service.visualize.visualize_top_of_views import get_views_of_top_of_day_of_week_chart
from ..service.visualize.visualize_videos_created import get_videos_created_by_day, get_videos_created_by_time_period, get_videos_created_by_year
from ..service.central_tendancy.get_mean_tendancy import means_of_save, means_of_share, means_of_view, means_of_duration, means_of_like, means_of_comment
from ..service.central_tendancy.get_median_tendancy import median_of_save, median_of_share, median_of_view, median_of_duration, median_of_like, median_of_comment
from ..service.central_tendancy.get_mode_tendancy import mode_of_save, mode_of_share, mode_of_view, mode_of_duration, mode_of_like, mode_of_comment

get_user_videos_analytics_bp = Blueprint('get_user_videos_analytics', __name__)

async def get_user_videos_analytics(user_name):
    """
    Get user videos data analytics and return it as JSON.
    
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
        data_loader = Dataloader(user_video_data["data"]["videos"])

        # Get dataframe
        df = data_loader.get_df()

        # Clean user videos data
        cleaned_data = clean_data(df)

        # Get distribution chart
        # print(cleaned_data)
        dist_chart = get_dis_chart(cleaned_data, 'Views')
        # dist_chart = get_views_of_top_of_day_of_week_chart(cleaned_data, 'Day of Week')
        # dist_chart = get_videos_created_by_year(cleaned_data, 1, 2, 'teal')
        # dist_chart = get_videos_created_by_day(cleaned_data, 1, 2, 'teal')
        # dist_chart = get_top_4_rows_and_other(cleaned_data, 'Views', 'teal')
        # dist_chart = get_heat_map_correlation_and_engagement_metrics(cleaned_data)
 
        # dist_chart = get_videos_created_by_time_period(df, "Create_year", 'greenyellow')

        # print(means_of_save(cleaned_data))
        # print(means_of_share(cleaned_data))
        # print(means_of_view(cleaned_data))
        # print(means_of_duration(cleaned_data))
        # print(means_of_like(cleaned_data))
        # print(means_of_comment(cleaned_data))
        # print(median_of_save(cleaned_data))
        # print(median_of_share(cleaned_data))
        # print(median_of_view(cleaned_data))
        # print(median_of_duration(cleaned_data))
        # print(median_of_like(cleaned_data))
        # print(median_of_comment(cleaned_data))
        # print(mode_of_save(cleaned_data))
        # print(mode_of_share(cleaned_data))
        # print(mode_of_view(cleaned_data))
        # print(mode_of_duration(cleaned_data))
        # print(mode_of_like(cleaned_data))
        # print(mode_of_comment(cleaned_data))
        

        # Set response data
        response.success = True
        response.message = "User videos data analytics has been generated successfully."
        response.data["displotUrl"] = dist_chart
        response.data["rowCount"] = len(cleaned_data)

        print(f"{Fore.GREEN}User videos data analytics has been generated successfully.")

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

