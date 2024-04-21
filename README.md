# Tikalyzer Flask Service

API for TikTok analyzing service

## Tech Stack

**Server:** Sure, it's Flask

## Installation

First, open TikTok on your browser and login. [https://www.tiktok.com]

Initially install with pip

```bash
    pip install TikTokApi
    python -m playwright install

```

Now if a small adjustment for your TikTok-API library so that it can works normally:

1. Go to `.venv/Lib/TikTokApi/api/user.py` or by `Crtl + Click` to the `user.videos()` method somewhere in the codes in VSCode.

2. Then go to line 188 in which the code looks like this:

```
    found = 0
    while found < count:
        params = {
            "secUid": self.sec_uid,
            "count": count,
            "cursor": cursor,
        }
```

3. Now change the `count` value to `35` like this:

```
    found = 0
    while found < count:
        params = {
            "secUid": self.sec_uid,
            "count": 35,
            "cursor": cursor,
        }
```

4. Voila, enjoy! Don't forget to `Ctrl + S`.

## Run Locally

Clone the project

```bash
  git clone https://github.com/lhphat02/tikalyzer-flask-service
```

Go to the project directory

```bash
  cd tikalyzer-flask-service
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  flask run
```

## API Reference

#### Get insights of an user's videos

```http
  GET /api/userVideoInsights?username=${username}
```

| Parameter  | Type     | Description                              |
| :--------- | :------- | :--------------------------------------- |
| `username` | `string` | **Required**. username of TikTok channel |

#### Get insights of a hashtag's videos

```http
  GET /api/hashtagVideoInsights?hashtag=${hashtag}
```

| Parameter   | Type     | Description                              |
| :---------- | :------- | :--------------------------------------- |
| `user_name` | `string` | **Required**. username of TikTok channel |

#### Get insights of trending videos

```http
  GET /api/trendingVideoInsights
```
