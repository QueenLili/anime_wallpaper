import aiohttp
import asyncio
from aiohttp import CookieJar


async def fetch(session, url):
    async with session.get(url) as response:
        print(response.cookies)
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session,  "https://anime-pictures.net/pictures/get_image/526673-2560x1440-vocaloid-ia+%28vocaloid%29-c.c.r-single-highres-wide+image.png"
)
        # print(html)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
