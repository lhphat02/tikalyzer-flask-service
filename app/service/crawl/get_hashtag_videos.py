from colorama import Fore
from TikTokApi import TikTokApi
from ...model.response import Response
from .import ms_token, chrome_path, format_data

async def get_hashtag_videos(hashtag, num_data=100):
    """
    Get hashtag videos data and return it as JSON.

    Args:
        hashtag (str): TikTok hashtag.
        num_data (int): Number of hashtag videos to retrieve.

    Returns:
        success (bool): True if the operation is successful, False otherwise.
        message (str): Response message.
        data (object): Response data (list of video dictionaries and row count).
    """

    cursor = 0
    response = Response()
    video_data_list = []

    async with TikTokApi() as api:
        # Create TikTok sessions
        await api.create_sessions(headless=True, ms_tokens=[ms_token], num_sessions=1, sleep_after=1, executable_path=chrome_path)

        tag = api.hashtag(name=hashtag)

        try:
            while cursor <= num_data:
                async for video in tag.videos(count=30, cursor=cursor):
                    # Initialize video data
                    video_data = format_data(video)

                    # Append video data to the list
                    video_data_list.append(video_data)

                    # Increment row count
                    cursor += 1

            # Set response data
            response.success = True
            response.message = "Hashtag videos data has been retrieved successfully."
            response.data["videos"] = video_data_list
            response.data["total"] = len(video_data_list)

            print(f"{Fore.GREEN}Hashtag videos data has been retrieved successfully.")

            return response.to_dict()

        except Exception as e:
            # Set response data
            response.message = e
            response.data = None

            print(f"{Fore.RED}Error: {e}")

            return response.to_dict()