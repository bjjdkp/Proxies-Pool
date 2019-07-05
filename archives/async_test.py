import asyncio
import requests
import aiohttp
import time
import threading
# import grequests

start = time.time()


async def get(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    result = await response.text()
    await session.close()
    return result


async def request():
    url = 'http://127.0.0.1:5000'
    print('Waiting for', url)
    result = await get(url)
    print('Get response from', url, 'Result:', result)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main(_):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:5000') as resp:
            print(resp.status)
            print(await resp.text())

# tasks = [main(_) for _ in range(3)]
# print(tasks)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))
# end = time.time()
# print('Cost time:', end - start)


# loop = asyncio.get_event_loop()
# tasks = [test() for i in range(3)]
# print(tasks)
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()


# async def get1():
#     loop = asyncio.get_event_loop()
#     future1 = loop.run_in_executor(None, requests.get, 'http://127.0.0.1:5000')

def func(url):
    print("send req")
    return requests.get(url)

async def pre(i):
    print("start req")
    # loop = asyncio.get_running_loop()
    future = await loop.run_in_executor(None, func, 'http://127.0.0.1:5000')

    print(future.text)

tasks = [asyncio.ensure_future(pre(i)) for i in range(3)]
print(tasks)
s_time = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

print("cost: %s" % (time.time()-s_time))

