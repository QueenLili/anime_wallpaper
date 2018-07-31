import asyncio
import os
import aiohttp
import aiofiles
import time
from threading import Thread

from PIL import Image

from gallery import random_picture
from picture import Picture


ASYNC_QUEUE = asyncio.Queue(5)
LOOP = asyncio.get_event_loop()


async def producer(func):
    while True:
        item = func()
        await ASYNC_QUEUE.put(item)
        print('Product:', item)
        await asyncio.sleep(1)


async def consumer():
    while True:
        item = await ASYNC_QUEUE.get()
        print('Consumed', item)
        if item and os.path.exists(item.file_path) and item.file_exist == '1':
            Wallpaper.SPARE_PICTURES.put(pic)
            print('已下载')
            pass
        else:
            async with aiohttp.ClientSession() as session:
                print('开始下载')
                async with session.get(item.url) as response:

                    async with aiofiles.open(item.file_path, 'wb') as fd:
                        data = await response.content.read()
                        await fd.write(data)
                print('下载完成')
            pic_data = Image.open(item.file_path)
            pic_data.save(item.file_path, 'BMP')
            mark_downloaded_tag(pic, '1')

def l():
    for _ in range(5):
        LOOP.create_task(producer(random_picture))
    for _ in range(5):
        LOOP.create_task(consumer())
    LOOP.run_forever()


t = Thread(target=l)
t.start()
print('--------------------')
time.sleep(1000)
