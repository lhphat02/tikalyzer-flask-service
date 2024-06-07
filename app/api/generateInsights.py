from flask import Flask, request, jsonify
import pandas as pd
import os
import asyncio
from dotenv import load_dotenv
from ..service.process_data.gemini_process_data import generate_tiktok_insights
from ..model.response import Response
from colorama import Fore

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

        print(f"{Fore.GREEN}TikTok insights have been generated successfully." + Fore.RESET)

        return response.to_dict()

    except Exception as e:
        response.message = str(e)
        response.data = None

        print(f"{Fore.RED}Error: {e}")

        return response.to_dict()

@generate_tiktok_insight_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        insights = loop.run_until_complete(process_file(file))
        return jsonify(insights)