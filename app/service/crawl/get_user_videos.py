import os
import json
from colorama import Fore
from TikTokApi import TikTokApi
from ...model.response import Response
from .import ms_token, chrome_path, format_data

async def get_user_videos(user_name, video_count):
    """
    Get user videos data and return it as JSON.
    
    Args:
        user_name (str): TikTok user name.
        video_count (int): The number of videos to retrieve.
        
    Returns:
    
        success (bool): True if the operation is successful, False otherwise.
        message (str): Response message.
        data (object): Response data (list of video dictionaries and row count).
    """

    response = Response()
    video_data_list = []
    data_dir = "data/json/user"
    file_path = f"{data_dir}/{user_name}_{video_count}_data.json"

    
    # Check if directory exists, if not create it
    directory = os.path.dirname(data_dir)
    if not os.path.exists(directory):
        os.makedirs(directory)


    # Check if data already exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            video_data_list = json.load(file)
        
        response.success = True
        response.message = "User videos data retrieved from storage."
        response.data["videos"] = video_data_list
        response.data["total"] = len(video_data_list)
        
        print(f"{Fore.GREEN}User videos data retrieved from storage.")
        return response.to_dict()

    async with TikTokApi() as api:
        # Create TikTok sessions 
        await api.create_sessions(headless=True, ms_tokens=[ms_token], num_sessions=1, sleep_after=1,executable_path=chrome_path)

        # Get user videos count
        user = api.user(user_name)
        post_count = video_count

        try:
            async for video in user.videos(count=post_count):
                # Initialize video data
                video_data = format_data(video)

                # Append video data to the list
                video_data_list.append(video_data)

            # Save data to JSON file
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as file:
                json.dump(video_data_list, file, indent=4)

            # Set response data
            response.success = True
            response.message = "User videos data has been retrieved and saved successfully."
            response.data["videos"] = video_data_list
            response.data["total"] = len(video_data_list)

            print(f"{Fore.GREEN}User videos data has been retrieved and saved successfully.")

            return response.to_dict()

        except Exception as e:
            # Set response data
            response.message = str(e)
            response.data = None

            print(f"{Fore.RED}Error: {e}")

            return response.to_dict()
