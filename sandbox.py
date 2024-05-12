from TikTokApi import TikTokApi
import asyncio
import json
import os

ms_token = os.environ.get("ms_token", None)

async def get_video_data(video_id):    
  async with TikTokApi() as api:
    await api.create_sessions(headless=True, ms_tokens=[ms_token], num_sessions=1, sleep_after=1, executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe")

    url = "https://www.tiktok.com/@sofm_official/video/7367645572137897224?is_from_webapp=1&sender_device=pc&web_id=7298271494848562689"
    video_info = await api.video(url=url).info()

    print(video_info)

    return video_info

def get_video_id(video_url):
    # Split the URL by '/' and '?' to get individual components
    parts = video_url.split('/')
    if len(parts) < 6:
        return None  # Not a valid TikTok URL
    # The video ID is the fourth last component
    video_id = parts[5].split('?')[0]
    return video_id

vid = get_video_id("https://www.tiktok.com/@sofm_official/video/7367645572137897224?is_from_webapp=1&sender_device=pc&web_id=7298271494848562689")


            
if __name__ == "__main__":
    asyncio.run(get_video_data(vid))