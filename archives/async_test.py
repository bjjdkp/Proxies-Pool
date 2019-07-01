import asyncio
import requests
import aiohttp
import time
import threading

start = time.time()


async def get(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    result = await response.text()
    await session.close()
    return result


async def request(i):
    url = 'http://127.0.0.1:5000'
    print('Waiting for', url)
    r = await asyncio.sleep(3)
    # response = await get(url)
    # print('Get response from', url, 'Result:', response)


tasks = [request(_) for _ in range(100)]
print(tasks)
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
end = time.time()
print('Cost time:', end - start)


async def hello():
    print('Hello world! (%s)' % threading.currentThread())
    await asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())


# loop = asyncio.get_event_loop()
# tasks = [hello(), hello()]
# print(tasks)
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()