"""
@Author: Jayce
@FileName: picture.py
@ProjectName: anime_wallpaper
@CreateTime: 2018/7/19 16:13
"""
import asyncio
import win32api
import win32gui
from queue import Queue
from threading import Lock
from threading import Thread
from urllib.parse import urljoin

import aiofiles
import aiohttp
import grequests
import win32con
from lxml import etree

from gallery import *
from picture import Picture
from srequests import Srequests

# 初始化图片库
Gallery()


class Wallpaper:
    # 图片网站
    HOST = 'https://anime-pictures.net'
    # 爬取网络请求并发数
    REQUEST_THREAD_NUMBER = 5
    # 爬取时间间隔
    SPIDER_TIME_INTERVAL = 60 * 60 * 3  # 3小时
    # 预准备图片个数
    SPARE_COUNT = 20
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
    ASYNC_QUEUE = asyncio.Queue(5)
    LOOP = asyncio.get_event_loop()


async def producer(func):
    while True:
        item = func()
        await Wallpaper.ASYNC_QUEUE.put(item)
        print('Product:', item)
        await asyncio.sleep(1)


async def consumer():
    while True:
        item = await Wallpaper.ASYNC_QUEUE.get()
        print('Consumed', item)
        if item and os.path.exists(item.file_path) and item.file_exist == '1':
            Wallpaper.SPARE_PICTURES.put(item)
            print('已下载')
            pass
        else:
            async with aiohttp.ClientSession() as session:
                print('开始下载')
                async with session.get(item.url) as response:
                    async with aiofiles.open(item.file_path, 'wb') as fd:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            await fd.write(chunk)
                print('下载完成')
            pic_data = Image.open(item.file_path)
            pic_data.save(item.file_path, 'BMP')
            mark_downloaded_tag(item, '1')
            Wallpaper.SPARE_PICTURES.put(item)


def async_prepare_wallpapers():
    for _ in range(5):
        Wallpaper.LOOP.create_task(producer(random_picture))
    for _ in range(5):
        Wallpaper.LOOP.create_task(consumer())
    Wallpaper.LOOP.run_forever()


# 获取图片详情url
def get_details_urls(text):
    html = etree.HTML(text)
    details_urls = html.xpath('//*[@id="posts"]/div[2]/span[*]/a/@href')
    return [urljoin(Wallpaper.HOST, _) for _ in details_urls]


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
    return [urljoin(Wallpaper.HOST, html.xpath(url_xpath)[0]), html.xpath(file_size_xpath)[0].strip(),
            html.xpath(resolution_ratio_xpath)[0], html.xpath(release_date_xpath)[0].strip()]


# 爬取图片
def picture_spider():
    srequest = Srequests()
    if srequest.check_cookies():
        pass
    else:
        print('update cookies ！')
        loginurl = 'https://anime-pictures.net/login/submit'
        logindata = {'login': 'jarvan', 'password': '55223636', 'time_zone': 'Asia/Shanghai'}
        srequest.update_cookies(loginurl, logindata)

    # 搜索图片
    taglist = ['girl', 'long hair', 'breasts', 'blush', 'light erotic']
    search_tag = '||'.join(taglist)

    # update_date 0：任何时候 1：上周 2：过去一个月 3：过去的一天
    if get_pictures_count() < 200:
        update_date = 0
    else:
        update_date = 2

    # search_url = "https://anime-pictures.net/pictures/view_posts/0?search_tag=%s&aspect=16:9&order_by=date&ldate=%d" \
    #              "&ext_jpg=jpg&ext_png=png&lang=en" % (search_tag, update_date)

    search_url = "https://anime-pictures.net/pictures/view_posts/0?search_tag=%s&res_x=1024&res_y=768&res_x_n=1&res_y_n=1&aspect=16:9&order_by=date&ldate=%d&small_prev=1&ext_jpg=jpg&ext_png=png&lang=en" % (
        search_tag, update_date)

    resp = srequest.session.get(search_url, headers=Srequests.headers).text
    # print(Srequests.headers)
    details_urls = []
    details_urls.extend(get_details_urls(resp))

    page_count = get_page_count(resp)

    search_urls = [
        "https://anime-pictures.net/pictures/view_posts/%d?search_tag=%s&res_x=1024&res_y=768&res_x_n=1&res_y_n=1&aspect=16:9&order_by=date&ldate=%d&small_prev=1&ext_jpg=jpg&ext_png=png&lang=en" % (
            x, search_tag, update_date) for x in range(1, int(page_count) + 1)]

    reqs = (grequests.get(url, headers=Srequests.headers, session=srequest.session) for url in search_urls)
    for r_data in grequests.imap(reqs, size=Wallpaper.REQUEST_THREAD_NUMBER):
        if r_data.status_code == 200:
            print('搜索页成功：' + r_data.url)
            details_urls.extend(get_details_urls(r_data.text))
        else:
            print('搜索页失败：' + r_data.url)

    # 图片详情页
    reqs = (grequests.get(url, headers=Srequests.headers, session=srequest.session) for url in details_urls)
    for r_data in grequests.imap(reqs, size=Wallpaper.REQUEST_THREAD_NUMBER):
        if r_data.status_code == 200:
            print('详情页成功：' + r_data.url)
            save_picture_info(Picture(*get_picture_info(r_data.text)))
        else:
            print('详情页失败：' + r_data.url)

    srequest.close()


# 爬取线程
def spider_thread():
    while True:
        picture_spider()
        time.sleep(Wallpaper.SPIDER_TIME_INTERVAL)


# 预备壁纸
def prepare_wallpapers():
    while True:
        print('当前预备图片个数：%d' % Wallpaper.SPARE_PICTURES.qsize())
        pic = random_picture()
        if pic:
            if pic.file_exist == '1' and os.path.exists(pic.file_path):
                Wallpaper.SPARE_PICTURES.put(pic)
            else:
                if download_picture(pic):
                    Wallpaper.SPARE_PICTURES.put(pic)
        else:
            time.sleep(1)


def random_set_wallpaper(hand_set=False):
    Wallpaper.LOCK.acquire()
    pic = Wallpaper.SPARE_PICTURES.get()
    print('更换壁纸...')
    print(os.path.abspath(pic.file_path))
    set_wallpaper(os.path.abspath(pic.file_path))
    if hand_set:
        Wallpaper.VIEW_HAND_PICTURES.put(pic)
        # time.sleep(Wallpaper.CHANGE_WALLPER_INTERVAL)
    else:
        Wallpaper.VIEW_AUTO_PICTURES.put(pic)
    Wallpaper.LOCK.release()


# 随机设置壁纸
def set_wallpaper_thread():
    while True:
        random_set_wallpaper()
        time.sleep(Wallpaper.CHANGE_WALLPER_INTERVAL)


# 设置壁纸
def set_wallpaper(picture):
    # 打开指定注册表路径
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    # 最后的参数:2拉伸,0居中,6适应,10填充,0平铺
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    # 最后的参数:1表示平铺,拉伸居中等都是0
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # 刷新桌面
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, picture, win32con.SPIF_SENDWININICHANGE)


if __name__ == '__main__':
    # 创建图片文件夹
    if not os.path.exists(Picture.DOWNLOAD_DIR):
        os.mkdir(Picture.DOWNLOAD_DIR)
    # 初始化图片库
    Gallery()
    # 爬虫线程
    t_spider = Thread(target=spider_thread)
    t_spider.start()
    # 预准备壁纸线程
    t_spare = Thread(target=prepare_wallpapers)
    t_spare.start()
    # 随机换壁纸
    t_wallpaper = Thread(target=set_wallpaper_thread)
    t_wallpaper.start()
    t_wallpaper.join()
