import asyncio
import aiohttp

async def fetch_img(session, url):
  with aiohttp.Timeout(10):
    async with session.get(url) as response:
      assert response.status == 200
      return await response.read()

loop = asyncio.get_event_loop()
with aiohttp.ClientSession(loop=loop) as session:
  img = loop.run_until_complete(
    fetch_img(session,'http://httpbin.org/image/png'))
  with open("img.png", "wb") as f:
    f.write(img)