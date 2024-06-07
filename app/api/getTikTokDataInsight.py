from flask import Flask, request, jsonify, make_response
import pandas as pd
import os
import asyncio
from dotenv import load_dotenv
from ..service.process_data.getTikTokDataInsight import generate_tiktok_insights
from ..model.response import Response
from colorama import Fore

from dotenv import load_dotenv

from flask import Blueprint, jsonify, request

generate_tiktok_insight_bp = Blueprint('generate_tiktok_insight_bp', __name__)

async def process_file(file):
    """
    Process the uploaded file and generate TikTok insights.

    Args:
        file (werkzeug.datastructures.FileStorage): The uploaded file.

    Returns:
        dict: The generated insights.
    """
    response = Response()

    try:
        print(f"{Fore.GREEN}PROCESS: Generating TikTok insights..." + Fore.RESET)
        df = pd.read_csv(file)
        insights = generate_tiktok_insights(df)

        response.success = True
        response.message = "TikTok insights have been generated successfully."
        response.data = insights

        print(insights)

        print(f"{Fore.GREEN}TikTok insights have been generated successfully." + Fore.RESET)

        return response.to_dict()

    except Exception as e:
        response.message = str(e)
        response.data = None

        print(f"{Fore.RED}Error: {e}")

        return response.to_dict()
        
API_KEY = os.getenv('API_KEY')

from flask import Response

@generate_tiktok_insight_bp.route('/upload', methods=['POST'])
def upload_file():
    print(f"check API key coi co gi ben route: {API_KEY}")
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
    #     loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(loop)
    #     insights = loop.run_until_complete(process_file(file))
        
        # Define your custom response
        custom_response = {
            "Video Performance Overview": {
                "The account boasts": 131,
                "Average likes": 4269,
                "Average comments": 45,
                "Average shares": 23,
                "Average views": 157763
            },
            "Video Duration": {
                "Videos range in length from": "0 to 106 seconds"
            },
            "Posting Frequency": {
                "Most active month": "May 2020",
                "Least active months": "Several with only 1 video each"
            },
            "Engagement by Day": {
                "Highest views": "Wednesdays",
                "Lowest views": "Mondays"
            },
            "Correlation Analysis": {
                "Weak negative correlation between duration and likes/views": True,
                "Weak negative correlation between duration and comments": True,
                "Weak positive correlation between duration and shares": True,
                "Overall, content and timing likely matter more than duration alone": True
            }
        }
        
        # Convert custom_response to HTML
        html_content = "<html><body><h1>Insights</h1>"
        for key, value in custom_response.items():
            html_content += f"<h2>{key}</h2><ul>"
            for sub_key, sub_value in value.items():
                html_content += f"<li>{sub_key}: {sub_value}</li>"
            html_content += "</ul>"
        html_content += "</body></html>"
        
        response = make_response(Response(html_content, mimetype='text/html'))
        response.headers["X-goog-api-key"] = API_KEY
        return response