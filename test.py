import asyncio
import random
import re
import time
import urllib
from urllib import request
import traceback
import async_timeout

import aiohttp


# import uvloop
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
def is_in_queue(item, q):
    if item in q:
        return True
    else:
        return False


async def run(url, urlq, kwdq2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    }
    try:
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(3):
                async with session.get(url, headers=headers) as response:
                    res = await response.text(encoding='utf-8')
                    keywords = re.findall(r'<a href="\?keyword=.*?htprequery=.*?">(.*?)</a>', res, re.S)
                    for keyword in keywords:
                        if not is_in_queue(keyword, kwdq2):
                            url = 'https://wap.sogou.com/web/searchList.jsp?keyword=%s' % urllib.request.quote(keyword)
                            urlq.append(url)
                            kwdq2.append(keyword)

    except:
        traceback.print_exc()
        print('网页打开失败')
        pass


while True:
    s = '电影'
    url = 'http://wap.sogou.com/web/searchList.jsp?keyword="%s"&pg=webSearchList' % urllib.request.quote(s)
    print(url)
    urlq = []
    kwdq2 = []
    urlq.append(url)
    print(urlq, kwdq2)
    while True:
        time_ = lambda: time.time()
        start = time_()
        tasks = []
        count = 0
        while count < 100:
            if not urlq == []:
                tempurl = urlq.pop(random.choice(range(0, len(urlq))))  # random.choice(urlq.queue[0]
                tasks.append(asyncio.ensure_future(run(tempurl, urlq, kwdq2)))
            if len(urlq) > 10000:
                for i in range(5000):
                    urlq.pop(random.choice(range(len(urlq))))
            if len(kwdq2) > 20000:
                for i in range(10000):
                    kwdq2.pop(random.choice(range(len(kwdq2))))
            count += 1
        print('url队列剩余{}'.format(len(urlq)))
        print('****' * 20)
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(asyncio.wait(tasks))
        except:
            print('over')
            break
        print('完成{}个Tasks的时间：{}秒'.format(count, time_() - start))
    print('sleeping..........')
    time.sleep(2)
