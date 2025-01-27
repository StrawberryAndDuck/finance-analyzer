import aiohttp


async def get(
    url: str,
    headers: dict | None = None,
    params: dict | None = None,
) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            return await response.json()


async def post(
    url: str,
    data: dict,
    headers: dict | None = None,
    auth: aiohttp.BasicAuth | None = None,
) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers, auth=auth) as response:
            return await response.json()
