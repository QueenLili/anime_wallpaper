"""
@Author: Jayce
@FileName: picture.py
@ProjectName: anime_wallpaper
@CreateTime: 2018/7/19 16:13
"""

import os

import grequests

from srequests import Srequests
from lxml import etree
from urllib.parse import urljoin
from picture import Picture

HOST = 'https://anime-pictures.net'


def get_details_urls(text):
    # 详情
    html = etree.HTML(text)
    details_urls = html.xpath('//*[@id="posts"]/div[2]/span[*]/a/@href')
    return [urljoin(HOST, _) for _ in details_urls]


def get_page_count(text):
    # 页码
    html = etree.HTML(text)
    html_data = html.xpath('//*[@id="posts"]/div[4]/form/p/text()[2]')
    page = html_data[0].strip()
    return page[page.rfind(' ') + 1:]


def get_picture_info(text):
    # 图片信息
    html = etree.HTML(text)
    release_date_xpath = '//*[@id="cont"]/div[1]/div[1]/text()[9]'
    resolution_ratio_xpath = '//*[@id="cont"]/div[1]/div[1]/a[2]/text()'
    file_size_xpath = '//*[@id="cont"]/div[1]/div[1]/text()[15]'
    url_xpath = '//*[@id="rating"]/a/@href'
    return [urljoin(HOST, html.xpath(url_xpath)[0]), html.xpath(release_date_xpath)[0].strip(),
            html.xpath(resolution_ratio_xpath)[0], html.xpath(file_size_xpath)[0].strip()]


if __name__ == '__main__':
    # 创建图片文件夹
    if not os.path.exists(Picture.DOWNLOAD_DIR):
        os.mkdir(Picture.DOWNLOAD_DIR)
    # exit()
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

    search_url = "https://anime-pictures.net/pictures/view_posts/0?search_tag=%s&aspect=16:9&order_by=date&ldate=0" \
                 "&ext_jpg=jpg&ext_png=png&lang=en" % search_tag
    resp = srequest.session.get(search_url, headers=Srequests.headers).text
    # print(Srequests.headers)
    pictures = []
    details_urls = []
    details_urls.extend(get_details_urls(resp))

    page_count = get_page_count(resp)

    # 搜索结果
    search_urls = ["https://anime-pictures.net/pictures/view_posts/%d?search_tag=%s&aspect=16:9&order_by=date&ldate=0" \
                   "&ext_jpg=jpg&ext_png=png&lang=en" % (x, search_tag) for x in range(1, int(page_count) + 1)]
    reqs = (grequests.get(url, headers=Srequests.headers, session=srequest.session) for url in search_urls)
    for r_data in grequests.imap(reqs, size=10):
        print(r_data)
        if r_data.status_code == 200:
            details_urls.extend(get_details_urls(r_data.text))
        else:
            print(r_data.url + '打开失败。')

    # 图片详情页
    reqs = (grequests.get(url, headers=Srequests.headers, session=srequest.session) for url in details_urls)
    for r_data in grequests.imap(reqs, size=10):
        print(r_data)
        if r_data.status_code == 200:
            Picture(*get_picture_info(r_data.text))
        else:
            print(r_data.url + '打开失败。')

    print(details_urls)
    print(pictures)
