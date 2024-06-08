from colorama import Fore
from TikTokApi import TikTokApi
from ...model.response import Response
from . import ms_token, chrome_path

async def get_video_info(video_url: str) -> dict:
    """
    Get video information from the given URL.

    Args:
        video_url (str): URL of the video.

    Returns:
        dict["success"] (bool): True if the operation is successful, False otherwise.
        dict["message"] (str): Response message.
        dict["data"] (object): Response data (video information dictionary).
    """

    response = Response()

    async with TikTokApi() as api:
        # Create TikTok sessions
        await api.create_sessions(headless=True, ms_tokens=[ms_token], num_sessions=1, sleep_after=1, executable_path=chrome_path)

        try:
            video = await api.video(url=video_url).info()

            response.success = True
            response.message = f"Video information retrieved successfully."
            response.data = video

            print(f"{Fore.GREEN}Video information retrieved successfully." + Fore.RESET)

            return response.to_dict()

        except Exception as e:
            response_data = {
                "success": False,
                "message": str(e),
                "data": None
            }

            print(f"{Fore.RED}Error: {e}" + Fore.RESET)

            return response_data
