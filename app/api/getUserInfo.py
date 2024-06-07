from flask import Blueprint, jsonify, request
from colorama import Fore
import asyncio

from ..model.response import Response as CustomResponse
from ..service.crawl.get_user_info import get_user_info

get_user_info_bp = Blueprint('get_user_info', __name__)

async def fetch_user_info(user_name):
    response = CustomResponse()

    try:
        print(f"{Fore.GREEN}PROCESS: Getting user information..." + Fore.RESET)
        user_info = await get_user_info(user_name)
        print(user_info)

        if not user_info["success"]:
            raise Exception(user_info["message"])

        response.success = True
        response.message = "User information fetched successfully."
        response.data = user_info["data"]

        return response.to_dict()
    
    except Exception as e:
        response.message = str(e)
        response.data = None
        print(f"{Fore.RED}Error: {e}")

        return response.to_dict()

@get_user_info_bp.route('/userInfo')
def user_info():
    user_name = request.args.get('user_name')
    if not user_name:
        return jsonify({"error": "user_name parameter is missing."}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    user_info_data = loop.run_until_complete(fetch_user_info(user_name))

    return jsonify(user_info_data)
