from colorama import Fore
from TikTokApi import TikTokApi
from ...model.response import Response
from .import ms_token, chrome_path, format_data


async def get_user_videos(user_name):
    """
    Get user videos data and return it as JSON.
    
    Args:
        user_name (str): TikTok user name.
        
    Returns:
        success (bool): True if the operation is successful, False otherwise.
        message (str): Response message.
        data (object): Response data (list of video dictionaries and row count).
    """

    response = Response()
    video_data_list = []

    async with TikTokApi() as api:
        # Create TikTok sessions 
        await api.create_sessions(headless=True, ms_tokens=[ms_token], num_sessions=1, sleep_after=1,executable_path=chrome_path)

        # Get user videos count
        user = api.user(user_name)
        user_data = await user.info()
        post_count = user_data["userInfo"]["stats"].get("videoCount")
        data_count = 1000 if post_count > 300 else post_count

        try:
            async for video in user.videos(count=data_count):
                # Initialize video data
                video_data = format_data(video)

                # Append video data to the list
                video_data_list.append(video_data)

            # Set response data
            response.success = True
            response.message = "User videos data has been retrieved successfully."
            response.data["videos"] = video_data_list
            response.data["total"] = len(video_data_list)

            print(f"{Fore.GREEN}User videos data has been retrieved successfully.")

            return response.to_dict()

        except Exception as e:
            # Set response data
            response.message = e
            response.data = None

            print(f"{Fore.RED}Error: {e}")

            return response.to_dict()
