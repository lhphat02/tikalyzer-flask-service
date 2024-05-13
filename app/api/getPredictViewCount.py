import asyncio

from flask import Blueprint, jsonify, request
from colorama import Fore
from ..model.response import Response
from ..service.machinelearning.get_predicted_view_count import get_predicted_view_count as get_predicted_view_count_service

get_predicted_view_count_bp = Blueprint('get_predicted_view_count', __name__)

async def get_predicted_view_count(video_url):
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
        # Predict view count
        print(f"{Fore.GREEN}PROCESS: Predicting view count..." + Fore.RESET)
        predicted_view_count = await get_predicted_view_count_service(video_url)

        # Set response data
        response.success = True
        response.message = "Predicted view count has been calculated successfully."
        response.data = predicted_view_count
        
        print(f"{Fore.GREEN}Predicted view count has been calculated successfully." + Fore.RESET)

        return response.to_dict()
    
    except Exception as e:
        # Set response data
        response.message = e
        response.data = None

        print(f"{Fore.RED}Error: {e}")

        return response.to_dict()
    

@get_predicted_view_count_bp.route('/predictedViewCount')
def get_prediction_data():
    # Get user name from the request parameters
    video_url = request.args.get('video_url')
    if not video_url:
        return jsonify({"error": "video_url parameter is missing."}), 400

    # Get user videos data
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    prediction_data = loop.run_until_complete(get_predicted_view_count(video_url))
    return jsonify(prediction_data)

