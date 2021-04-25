import asyncio

from aiohttp import ClientSession
from bs4 import BeautifulSoup


class Posts:
    URL_PREFIX = "https://city4people.ru"
    URLS = {
        "tram": "/tag/трамвай",
        "trolley": "/tag/троллейбус",
        "zero_deaths": "/tag/vision+zero",
        "bicycles": "/tag/велосипеды",
        "walkers": "/tag/пешеходы",
        "all_posts": "",
    }

    async def get(self, url):
        async with ClientSession() as session:
            res = await session.get(self.URL_PREFIX + "/posts" + url)
            self.soup = BeautifulSoup(await res.text(), 'html.parser')

        return self._parse()

    def _parse(self):
        posts = []

        for size in (4, 6):
            for row in self.soup.find_all("div", class_=f"col-lg-{size}"):
                try:
                    link = row.find("div", class_="project-item").h3.a
                except AttributeError:
                    continue

                posts.append({"name": link.text,
                              "url": self.URL_PREFIX + link["href"]})

        return posts



async def main():
    posts = Posts()

    print(await posts.get(posts.URLS["tram"]))


if __name__ == "__main__":
    asyncio.run(main())
