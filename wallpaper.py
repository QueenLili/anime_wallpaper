"""
@Author: Jayce
@FileName: picture.py
@ProjectName: anime_wallpaper
@CreateTime: 2018/7/19 16:13
"""

import time
import win32api
import win32gui
from threading import Thread
from urllib.parse import urljoin

import grequests
import win32con
from lxml import etree

from gallery import *
from picture import Picture
from srequests import Srequests

# 图片网站
HOST = 'https://anime-pictures.net'
# 爬取网络请求并发数
REQUEST_THREAD_NUMBER = 5
# 爬取时间间隔
SPIDER_TIME_INTERVAL = 60 * 60 * 3  # 3小时
# 预准备图片列表
SPARE_PICTURES = []
# 预准备图片个数
SPARE_COUNT = 20
# 更换壁纸频率
CHANGE_WALLPER_INTERVAL = 60 * 1  # 1分钟


# 获取图片详情url
def get_details_urls(text):
    # 详情
    html = etree.HTML(text)
    details_urls = html.xpath('//*[@id="posts"]/div[2]/span[*]/a/@href')
    return [urljoin(HOST, _) for _ in details_urls]


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
    return [urljoin(HOST, html.xpath(url_xpath)[0]), html.xpath(file_size_xpath)[0].strip(),
            html.xpath(resolution_ratio_xpath)[0], html.xpath(release_date_xpath)[0].strip()]


# 爬取图片
def picture_spider():
    Gallery()
    srequest = Srequests()
    if srequest.check_cookies():
        pass
    else:
        print('update cookies ！')
        loginurl = 'https://anime-pictures.net/login/submit'
        logindata = {'login': 'jarvan', 'password': '55223636', 'time_zone': 'Asia/Shanghai'}
        srequest.update_cookies(loginurl, logindata)

    # 搜索图片
    taglist = ['girl', 'long hair', 'breasts', 'blush', 'single', 'light erotic']
    search_tag = '||'.join(taglist)

    # update_date 0：任何时候 1：上周 2：过去一个月 3：过去的一天
    if get_pictures_count() < 200:
        update_date = 0
    else:
        update_date = 2

    search_url = "https://anime-pictures.net/pictures/view_posts/0?search_tag=%s&aspect=16:9&order_by=date&ldate=%d" \
                 "&ext_jpg=jpg&ext_png=png&lang=en" % (search_tag, update_date)
    resp = srequest.session.get(search_url, headers=Srequests.headers).text
    # print(Srequests.headers)
    details_urls = []
    details_urls.extend(get_details_urls(resp))

    page_count = get_page_count(resp)

    # 搜索结果
    search_urls = ["https://anime-pictures.net/pictures/view_posts/%d?search_tag=%s&aspect=16:9&order_by=date&ldate=0" \
                   "&ext_jpg=jpg&ext_png=png&lang=en" % (x, search_tag) for x in range(1, int(page_count) + 1)]
    reqs = (grequests.get(url, headers=Srequests.headers, session=srequest.session) for url in search_urls)
    for r_data in grequests.imap(reqs, size=REQUEST_THREAD_NUMBER):
        print(r_data)
        if r_data.status_code == 200:
            details_urls.extend(get_details_urls(r_data.text))
        else:
            print(r_data.url + '该页打开失败。')

    # 图片详情页
    reqs = (grequests.get(url, headers=Srequests.headers, session=srequest.session) for url in details_urls)
    for r_data in grequests.imap(reqs, size=REQUEST_THREAD_NUMBER):
        print(r_data)
        if r_data.status_code == 200:
            save_picture_info(Picture(*get_picture_info(r_data.text)))
        else:
            print(r_data.url + '详情页面打开失败。')

    # print(details_urls)
    srequest.close()


# 爬取线程
def spider_thread():
    while True:
        picture_spider()
        time.sleep(SPIDER_TIME_INTERVAL)


# 预备壁纸
def prepare_wallpapers():
    while True:
        print(SPARE_PICTURES)
        while len(SPARE_PICTURES) < SPARE_COUNT:
            pic = random_picture()
            if pic.file_exist != '1':
                if download_picture(pic):
                    SPARE_PICTURES.append(pic)
        time.sleep(1)


# 随机设置壁纸
def random_set_wallpaper(time_seg):
    while True:
        if SPARE_PICTURES:
            pic = SPARE_PICTURES[0]
            set_wallpaper(os.path.abspath(pic.file_path))
            SPARE_PICTURES.pop(0)
            time.sleep(time_seg)
        else:
            time.sleep(1)


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
    # exit()
    t_spider = Thread(target=spider_thread)
    t_spider.start()
    t_spare = Thread(target=prepare_wallpapers)
    t_spare.start()

    random_set_wallpaper(30)
