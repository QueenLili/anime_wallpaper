import asyncio
import os

from gallery import random_picture


class AsyncEventQueue:
    def __init__(self, func):
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue(loop=self.loop)
        self.producer_coro = self.produce(func)
        self.consumer_coro = self.consume()

    async def produce(self, func):
        while True:
            # produce an item
            a = func()
            print(a)
            # simulate i/o operation using sleep
            await asyncio.sleep(1)
            # put the item in the queue
            await self.queue.put(a)

    async def consume(self):
        while True:
            # wait for an item from the producer
            item = await self.queue.get()
            if item and os.path.exists(item.file_path) and item.file_exist == '1':
                # Wallpaper.SPARE_PICTURES.put(pic)
                pass

            else:

                # process the item
                print('consuming item...', item)
                # simulate i/o operation using sleep
                await asyncio.sleep(1)

    def main(self):
        self.loop.run_until_complete(asyncio.gather(self.producer_coro, self.consumer_coro))
        self.loop.close()


l = AsyncEventQueue(random_picture)
l.main()
