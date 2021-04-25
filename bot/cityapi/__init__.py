from .posts import Posts

import asyncio


post_cache = {}
posts = Posts()


async def main():
    for tag in list(posts.URLS.keys()):
        post_cache[tag] = await posts.get(posts.URLS[tag])


asyncio.run(main())
