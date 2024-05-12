import asyncio

from flask import Blueprint, jsonify, request
from colorama import Fore

from ..model.response import Response
from ..model.data_loader import Dataloader
from ..service.crawl.get_user_videos import get_user_videos
from ..service.clean.clean_df import clean_data
from ..service.visualize.visualize_distribution import get_dis_chart
from ..service.visualize.visualize_heat_map_correlation import get_heat_map_correlation_and_engagement_metrics
from ..service.visualize.visualize_top_of_views import get_views_of_top_of_day_of_week_chart
from ..service.visualize.visualize_top_4 import get_top_size_pie_chart
from ..service.visualize.visualize_videos_created import get_videos_created_by_year, get_videos_created_by_month
from ..service.visualize.visualize_videos_created import get_videos_created_by_day

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
        print(f"{Fore.GREEN}PROCESS: Scraping user videos data..." + Fore.RESET)
        user_video_data = await get_user_videos(user_name)
        data_loader = Dataloader(user_video_data["data"]["videos"])

        # Get dataframe
        print(f"{Fore.GREEN}PROCESS: Getting user videos data as a dataframe..." + Fore.RESET)
        df = data_loader.get_df()

        # Clean user videos data
        cleaned_data = clean_data(df)

        # Get charts
        print(f"{Fore.GREEN}PROCESS: Generating user videos data analytics..." + Fore.RESET)

        dist_chart = get_dis_chart(cleaned_data, 'Views')        
        heat_map = get_heat_map_correlation_and_engagement_metrics(cleaned_data)
        top_day_of_week_chart = get_views_of_top_of_day_of_week_chart(cleaned_data, 'Views')
        top_size_pie_chart = get_top_size_pie_chart(cleaned_data)
        year_create_chart = get_videos_created_by_year(cleaned_data)
        month_create_chart = get_videos_created_by_month(cleaned_data)
        day_create_chart = get_videos_created_by_day(cleaned_data)
        
        # Get statistic calculations
        print(f"{Fore.GREEN}PROCESS: Calculating statistics..." + Fore.RESET)

        mean = cleaned_data['Views'].mean()
        median = cleaned_data['Views'].median()
        mode = cleaned_data['Views'].mode().values[0]

        # Set response data
        response.success = True
        response.message = "User videos data analytics has been generated successfully."
        response.data["displotUrl"] = dist_chart
        response.data["heatmapUrl"] = heat_map
        response.data["topDayOfWeekUrl"] = top_day_of_week_chart
        response.data["topSizePieChartUrl"] = top_size_pie_chart
        response.data["yearCreateChartUrl"] = year_create_chart
        response.data["monthCreateChartUrl"] = month_create_chart
        response.data["dayCreateChartUrl"] = day_create_chart
        response.data["mean"] = mean
        response.data["median"] = median
        response.data["mode"] = mode
        response.data["rowCount"] = len(cleaned_data)
        
        print(f"{Fore.GREEN}User videos data analytics has been generated successfully." + Fore.RESET)

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

