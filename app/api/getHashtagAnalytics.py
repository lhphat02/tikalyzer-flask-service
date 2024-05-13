import asyncio
from flask import Blueprint, jsonify, request
from colorama import Fore

from ..model.response import Response
from ..model.data_loader import Dataloader
from ..service.crawl.get_hashtag_videos import get_hashtag_videos
from ..service.clean.clean_df import clean_data
from ..service.visualize.visualize_distribution import get_dis_chart
from ..service.visualize.visualize_heat_map_correlation import get_heat_map_correlation_and_engagement_metrics
from ..service.visualize.visualize_top_dow import get_views_of_top_of_day_of_week_chart
from ..service.visualize.visualize_top_size import get_top_size_pie_chart
from ..service.visualize.visualize_videos_created import get_videos_created_by_year, get_videos_created_by_month
from ..service.visualize.visualize_videos_created import get_videos_created_by_day


get_hashtag_videos_analytics_bp = Blueprint('get_hashtag_videos_analytics', __name__)

async def get_hashtag_videos_analytics(hashtag):
    """
    Get hashtag videos data analytics and return it as JSON.
    
    Args:
        hashtag (str): TikTok hashtag name.
        
    Returns:
        dict["success"] (bool): True if the hashtag videos data has been saved to a CSV file, False otherwise.
        dict["message"] (str): Response message.
        dict["data"] (object): Response data.
    """

    response = Response()

    try:
        # Scrape hashtag videos data
        hashtag_video_data = await get_hashtag_videos(hashtag)
        data_loader = Dataloader(hashtag_video_data["data"]["videos"])

        # Get dataframe
        df = data_loader.get_df()

        # Clean hashtag videos data
        cleaned_data = clean_data(df)

        # Get charts
        dist_chart = get_dis_chart(cleaned_data, 'Views')        
        heat_map = get_heat_map_correlation_and_engagement_metrics(cleaned_data)
        top_day_of_week_chart = get_views_of_top_of_day_of_week_chart(cleaned_data)
        top_size_pie_chart = get_top_size_pie_chart(cleaned_data)
        year_create_chart = get_videos_created_by_year(cleaned_data)
        month_create_chart = get_videos_created_by_month(cleaned_data)
        day_create_chart = get_videos_created_by_day(cleaned_data)
        
        # Get statistic calculations
        mean = cleaned_data['Views'].mean()
        median = cleaned_data['Views'].median()
        mode = cleaned_data['Views'].mode().values[0]

        # Set response data
        response.success = True
        response.message = "Hashtag videos data analytics has been generated successfully."
        response.data["displotUrl"] = dist_chart
        response.data["heatmapUrl"] = heat_map
        response.data["topDayOfWeekUrl"] = top_day_of_week_chart
        response.data["topSizePieChartUrl"] = top_size_pie_chart
        response.data["yearCreateChartUrl"] = year_create_chart
        response.data["monthCreateChartUrl"] = month_create_chart
        response.data["dayCreateChartUrl"] = day_create_chart
        response.data["mean"] = float(mean)  
        response.data["median"] = float(median)  
        response.data["mode"] = int(mode)  
        response.data["rowCount"] = len(cleaned_data)
        
        print(f"{Fore.GREEN}Hashtag videos data analytics has been generated successfully." + Fore.RESET)

        return response.to_dict()
    
    except Exception as e:
        # Set response data
        response.message = e
        response.data = None

        print(f"{Fore.RED}Error: {e}")

        return response.to_dict()
    

@get_hashtag_videos_analytics_bp.route('/hashtagVideosAnalytics')
def hashtag_videos_analytics():
    # Get hashtag name from the request parameters
    hashtag = request.args.get('hashtag')
    if not hashtag:
        return jsonify({"error": "Hashtag parameter is missing."}), 400

    # Get hashtag videos data
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    hashtag_videos_data = loop.run_until_complete(get_hashtag_videos_analytics(hashtag))
    return jsonify(hashtag_videos_data)

