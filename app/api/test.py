import asyncio

from flask import Blueprint, jsonify, request
from colorama import Fore

from ..model.response import Response
from ..model.data_loader import Dataloader
from ..service.crawl.get_user_videos import get_user_videos
from ..service.crawl.get_trending_videos import get_trending_videos
from ..service.clean.clean_df import clean_data
from ..service.visualize.visualize_distribution import get_dis_chart

get_test_bp = Blueprint('get_test', __name__)

async def get_test():
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
        trending_video_data = await get_trending_videos()
        data_loader = Dataloader(trending_video_data["data"]["videos"])

        # Get dataframe
        df = data_loader.get_df()

        # Clean user videos data
        cleaned_data = clean_data(df)



        # YOUR CODE HERE:
        # dist_chart = get_dis_chart(cleaned_data, 'Views')
        # response.data["displotUrl"] = dist_chart
        #
        #
        #
        #
        hello_world = "Hello World"
        response.data["helloWorld"] = hello_world


        
        # Set response data
        response.success = True
        response.message = "User videos data analytics has been generated successfully."
        response.data["rowCount"] = len(cleaned_data)

        print(f"{Fore.GREEN}User videos data analytics has been generated successfully.")

        return response.to_dict()
    
    except Exception as e:
        # Set response data
        response.message = e
        response.data = None

        print(f"{Fore.RED}Error: {e}")

        return response.to_dict()
    

@get_test_bp.route('/getTest')
def user_videos_analytics():
    # Get user videos data
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    test_data = loop.run_until_complete(get_test())
    return jsonify(test_data)

