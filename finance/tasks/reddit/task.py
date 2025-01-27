import asyncio
import datetime
import os

import aiohttp

from finance.async_requests import get, post
from finance.tasks.reddit.constants import API_URL_REDDIT, API_URL_REDDIT_OAUTH
from finance.tasks.reddit.logger import logger


async def fetch_token(
    username: str,
    password: str,
    client_id: str,
    client_secret: str,
) -> str:
    response = await post(
        url=f"{API_URL_REDDIT}/api/v1/access_token",
        data={
            "grant_type": "password",
            "username": username,
            "password": password,
        },
        auth=aiohttp.BasicAuth(
            client_id,
            client_secret,
        ),
    )
    return response["access_token"]


def reddit_token(func):
    async def wrapper(*args, **kwargs):
        token = await fetch_token(
            username=os.getenv("REDDIT_USERNAME"),
            password=os.getenv("REDDIT_PASSWORD"),
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        )
        return await func(token=token, *args, **kwargs)

    return wrapper


@reddit_token
async def fetch(
    token: str,
    url: str,
    params: dict | None = None,
) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
    }
    return await get(
        url=url,
        headers=headers,
        params=params,
    )


async def fetch_best_posts() -> list[dict]:
    return await fetch(
        url=f"{API_URL_REDDIT_OAUTH}/best",
    )


async def fetch_queried_posts(
    query: str,
    sort: str = "top",
    recent: str = "day",
    limit: int = 100,
) -> dict:
    return await fetch(
        url=f"{API_URL_REDDIT_OAUTH}/search",
        params={
            "q": query,
            "sort": sort,
            "t": recent,
            "limit": limit,
        },
    )


async def retrieve_queried_text_contents(
    query: str,
    sort: str = "top",
    recent: str = "day",
    limit: int = 100,
) -> list[dict]:
    response = await fetch_queried_posts(
        query=query,
        sort=sort,
        recent=recent,
        limit=limit,
    )
    children = response["data"]["children"]
    filtered_children = filter(lambda post: post["data"]["selftext"], children)
    return [
        {
            "title": post["data"]["title"],
            "selftext": post["data"]["selftext"],
            "permalink": f"{API_URL_REDDIT}{post['data']['permalink']}",
            "created_utc": datetime.datetime.utcfromtimestamp(
                post["data"]["created_utc"]
            ),
        }
        for post in filtered_children
    ]


async def monitoring(query: str, interval: int = 60):
    while True:
        contents = await retrieve_queried_text_contents(query=query)
        for content in contents:
            logger.info(
                f"{content['title']}|\n{content['created_utc']}|\n{content['permalink']}|\n{content['selftext']}"
            )
            await asyncio.sleep(interval)


async def add_reddit_tasks(topics: list[str]):
    for topic in topics:
        asyncio.create_task(monitoring(query=topic, interval=10))
