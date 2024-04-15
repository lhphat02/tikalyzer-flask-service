from TikTokApi import TikTokApi
import asyncio
import time
import os
from datetime import datetime


ms_token = os.environ.get("ms_token", None)


async def get_trending_videos(num_data=300):
    videos_data = []
    cursor = 0

    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)

        while cursor <= num_data:
            async for video in api.trending.videos(count=30, cursor=cursor):
                print(video)
                video_data = video.as_dict
                videos_data.append(video_data) 
            cursor += 30
    return videos_data


async def get_hashtag_videos(hash_tag, num_data=300):
    cursor = 0

    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=True, executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe")
        tag = api.hashtag(name=hash_tag)

        with open(f"csv/hashtag_{hash_tag}_{num_data}.csv" , "w", encoding='utf-8') as f:
            header_labels = "Create_time,Create_year,Create_month,Create_day,Create_hour,Likes,Comments,Saves,Views,Shares,Duration(sec),Video Height,Video Width\n"
            f.write(header_labels)

            while cursor <= num_data:
                async for video in tag.videos(count=30, cursor=cursor):
                    create_time = str(video.create_time)
                    video_data = {
                        "Create_time": video.create_time,
                        "Create_year": create_time[0:4],
                        "Create_month": create_time[5:7],
                        "Create_day": create_time[8:10],
                        "Create_hour": create_time[11:13],
                        "Likes": video.stats["diggCount"],
                        "Comments": video.stats["commentCount"],
                        "Saves": video.stats["collectCount"],
                        "Views": video.stats["playCount"],
                        "Shares": video.stats["shareCount"],
                        "Duration(sec)": video.as_dict["video"]["duration"],
                        "Video Height": video.as_dict["video"]["height"],
                        "Video Width": video.as_dict["video"]["width"],
                    }
                    row = f'{video_data["Create_time"]},"{video_data["Create_year"]}","{video_data["Create_month"]}","{video_data["Create_day"]}","{video_data["Create_hour"]}","{video_data["Likes"]}","{video_data["Comments"]}",{video_data["Saves"]},{video_data["Views"]},{video_data["Shares"]},{video_data["Duration(sec)"]},{video_data["Video Height"]},{video_data["Video Width"]}\n'
                    f.write(row)
                cursor += 30


async def get_user_videos_legacy(user_name, num_data=300): # not working
    result = []
    cursor = 0

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")[0:10].replace("-", "")


    print(f"Current date: {current_date}")
            
    return result

async def get_user_videos(username):
    start_time = time.time()
    row_count = 0

    async with TikTokApi() as api:
        await api.create_sessions(headless=True, ms_tokens=[ms_token], num_sessions=1, sleep_after=3,executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe")
        user = api.user(username)
        user_data = await user.info()
        post_count = user_data["userInfo"]["stats"].get("videoCount")

        with open(f"csv/user_videos_{username}.csv" , "w", encoding='utf-8') as f:
            header_labels = "Create_time,Create_year,Create_month,Create_day,Create_hour,Likes,Comments,Saves,Views,Shares,Duration(sec),Video Height,Video Width\n"
            f.write(header_labels)

            async for video in user.videos(count=post_count):
                create_time = str(video.create_time)
                video_data = {
                    "Create_time": video.create_time,
                    "Create_year": create_time[0:4],
                    "Create_month": create_time[5:7],
                    "Create_day": create_time[8:10],
                    "Create_hour": create_time[11:13],
                    "Likes": video.stats["diggCount"],
                    "Comments": video.stats["commentCount"],
                    "Saves": video.stats["collectCount"],
                    "Views": video.stats["playCount"],
                    "Shares": video.stats["shareCount"],
                    "Duration(sec)": video.as_dict["video"]["duration"],
                    "Video Height": video.as_dict["video"]["height"],
                    "Video Width": video.as_dict["video"]["width"],
                }
                row = f'{video_data["Create_time"]},"{video_data["Create_year"]}","{video_data["Create_month"]}","{video_data["Create_day"]}","{video_data["Create_hour"]}","{video_data["Likes"]}","{video_data["Comments"]}",{video_data["Saves"]},{video_data["Views"]},{video_data["Shares"]},{video_data["Duration(sec)"]},{video_data["Video Height"]},{video_data["Video Width"]}\n'
                f.write(row)
                
                url = f"https://www.tiktok.com/@{video.as_dict['author']['uniqueId']}/video/{video.id}"
                print(f"URL: {url}") 
                row_count += 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time} seconds")
    print(f"Total rows: {row_count}")
    print(f"Rows per second: {row_count / elapsed_time}")

    

            
if __name__ == "__main__":
    asyncio.run(get_trending_videos(100))
    # asyncio.run(get_hashtag_videos("sofm", 150))
    # asyncio.run(get_user_videos_legacy("sofm_official", 150))
    asyncio.run(get_user_videos("sofm_official"))