from colorama import Fore
from TikTokApi import TikTokApi
from ...model.response import Response
from .import ms_token, chrome_path


async def get_user_info(user_name):
    """
    Get user information.

    Args:
        user_name (str): TikTok user name.

    Returns:
        dict["success"] (bool): True if the operation is successful, False otherwise.
        dict["message"] (str): Response message.
        dict["data"] (object): Response data (user information dictionary).
    """

    response = Response()

    async with TikTokApi() as api:
        # Create TikTok sessions
        await api.create_sessions(headless=True, ms_tokens=[ms_token], num_sessions=1, sleep_after=1, executable_path=chrome_path)

        try:
            user = api.user(user_name)
            user_data = await user.info()

            response.success = True
            response.message = f"{user_name} user information retrieved successfully."
            response.data = user_data


            print(f"{Fore.GREEN}{user_name} user information retrieved successfully." + Fore.RESET)

            return response.to_dict()

        except Exception as e:
            response_data = {
                "success": False,
                "message": str(e),
                "data": None
            }

            print(f"{Fore.RED}Error: {e}" + Fore.RESET)

            return response_data
