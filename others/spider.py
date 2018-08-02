"""
@Author: Mr. Li
@Software: PyCharm
@FileName: spider_queue.py
@CreateTime: 2018/8/2 22:16
"""

from queue import PriorityQueue
from queue import Queue
from threading import Lock
from threading import Thread
from urllib.parse import urljoin
from requests import Timeout
import requests
from lxml import etree

from cookie import Cookie
from gallery import *
from picture import Picture

# 初始化图片库
# Gallery()
Cookie()


# 创建队列实例， 用于存储任务


class Spider:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }    # 图片网站
    HOST = 'https://anime-pictures.net'
    # 超时时间
    TIMEOUT = 30
    # 爬取网络请求并发数
    REQUEST_THREAD_NUMBER = 5
    # 爬取时间间隔
    SPIDER_TIME_INTERVAL = 60 * 60 * 3  # 3小时
    # 预准备图片个数
    SPARE_COUNT = 20
    # 爬虫优先级队列 0：高优先（图片详情） 1：低优先（搜索结果页）
    SPIDER_QUEUE = PriorityQueue()

    # 预准备图片队列
    SPARE_PICTURES = Queue(SPARE_COUNT)  # 指定队列大小
    # 界面显示自动图片队列
    VIEW_AUTO_PICTURES = Queue()
    # 界面显示手动图片队列
    VIEW_HAND_PICTURES = Queue()
    # 更换壁纸频率
    CHANGE_WALLPER_INTERVAL = 10  # 60秒
    CHANGE_WALLPER_INTERVAL = get_change_wallper_interval(CHANGE_WALLPER_INTERVAL)
    # 更换图片线程锁
    LOCK = Lock()


# 获取图片详情url
def get_details_urls(text):
    html = etree.HTML(text)
    details_urls = html.xpath('//*[@id="posts"]/div[2]/span[*]/a/@href')
    return [urljoin(Spider.HOST, _) for _ in details_urls]


# 获取搜索结果页码
def get_page_count(text):
    # 页码
    html = etree.HTML(text)
    html_data = html.xpath('//*[@id="posts"]/div[4]/form/p/text()[2]')
    page = html_data[0].strip()
    return page[page.rfind(' ') + 1:]


# 获取图片信息
def get_picture_info(text):
    # 图片信息
    html = etree.HTML(text)
    release_date_xpath = '//*[@id="cont"]/div[1]/div[1]/text()[9]'
    resolution_ratio_xpath = '//*[@id="cont"]/div[1]/div[1]/a[2]/text()'
    file_size_xpath = '//*[@id="cont"]/div[1]/div[1]/text()[15]'
    url_xpath = '//*[@id="rating"]/a/@href'
    return [urljoin(Spider.HOST, html.xpath(url_xpath)[0]), html.xpath(file_size_xpath)[0].strip(),
            html.xpath(resolution_ratio_xpath)[0], html.xpath(release_date_xpath)[0].strip()]


# 爬取图片
def spider_work():
    while True:
        try:
            level, url = Spider.SPIDER_QUEUE.get()
            if level == 1:
                # 搜索结果页
                reqs = requests.get(url, headers=Spider.HEADERS, cookies=Cookie.cookies, timeout=Spider.TIMEOUT)
                if reqs.status_code == 200:
                    print('搜索页成功：' + url)
                    for details_url in get_details_urls(reqs.text):
                        Spider.SPIDER_QUEUE.put((0, details_url))
                else:
                    print('搜索页失败：' + url)
            elif level == 0:
                # 图片详情页
                reqs = requests.get(url, headers=Spider.HEADERS, cookies=Cookie.cookies)
                if reqs.status_code == 200:
                    print('详情页成功：' + url)
                    save_picture_info(Picture(*get_picture_info(reqs.text)))
                else:
                    print('详情页失败：' + url)
            else:
                pass
        except Timeout as e:
            print(e)
        except Exception as e:
            print(e)
        finally:
            Spider.SPIDER_QUEUE.task_done()


def picture_spider():
    # 创建线程池
    [Thread(target=spider_work, daemon=True).start() for _ in range(Spider.REQUEST_THREAD_NUMBER)]
    while True:
        # 搜索图片
        taglist = ['girl', 'long hair', 'breasts', 'blush', 'light erotic']
        search_tag = '||'.join(taglist)

        # update_date 0：任何时候 1：上周 2：过去一个月 3：过去的一天
        if get_pictures_count() > 200:
            update_date = 0
        else:
            update_date = 2
        # 第一页结果
        search_url = "https://anime-pictures.net/pictures/view_posts/0?search_tag=%s&res_x=1024&res_y=768&res_x_n=1&res_y_n=1&aspect=16:9&order_by=date&ldate=%d&small_prev=1&ext_jpg=jpg&ext_png=png&lang=en" % (
            search_tag, update_date)
        try:
            reqs = requests.get(search_url, headers=Spider.HEADERS, cookies=Cookie.cookies)
            if reqs.status_code == 200:
                text = reqs.text
                print('搜索页成功：' + search_url)
                for details_url in get_details_urls(text):
                    Spider.SPIDER_QUEUE.put((0, details_url))
                page_count = get_page_count(reqs.text)
                for x in range(1, int(page_count) + 1):
                    Spider.SPIDER_QUEUE.put((1, "https://anime-pictures.net/pictures/view_posts/%d?search_tag=%s&res_x=1024&res_y=768&res_x_n=1&res_y_n=1&aspect=16:9&order_by=date&ldate=%d&small_prev=1&ext_jpg=jpg&ext_png=png&lang=en" % (x, search_tag, update_date)))
        except Timeout as e:
            print(e)
        except Exception as e:
            print(e)
        finally:
            Spider.SPIDER_QUEUE.join()
            print('----------------------------')
        time.sleep(5)





if __name__ == '__main__':
    # queue = Queue()
    # # 定义需要线程池执行的任务
    # def do_job():
    #     while True:
    #         _, i = queue.get()
    #         time.sleep(1)
    #         print('index %s, curent: %s' % (i, threading.current_thread()))
    #         if i % 2 == 0:
    #             queue.put((0, 333))
    #         queue.task_done()
    # # 创建包括3个线程的线程池
    # for i in range(3):
    #     t = Thread(target=do_job)
    #     t.daemon = True  # 设置线程daemon  主线程退出，daemon线程也会推出，即时正在运行
    #     t.start()
    #
    # # 模拟创建线程池3秒后塞进10个任务到队列
    # def a():
    #     i = 0
    #     for i in range(10):
    #         queue.put((1, i))
    #         i += 1
    #
    #
    # t = Thread(target=a)
    # t.start()
    # t.join()
    # queue.join()
    # a()
    # queue.join()



    # 爬虫线程
    t_spider = Thread(target=picture_spider)
    t_spider.start()
    t_spider.join()

    time.sleep(99999)
