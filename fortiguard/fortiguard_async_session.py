import aiohttp
import asyncio

from settings import TEST_URLS

async def fetch(session, url, sema):
    async with sema, session.get(url) as response:
        return await response.text()

async def main():
    urls = TEST_URLS
    tasks = []
    sema = asyncio.BoundedSemaphore(value=100)
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(fetch(session, url, sema))
            # print(url)
        htmls = await asyncio.gather(*tasks)
        for html in htmls:
            print(html[:100])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())