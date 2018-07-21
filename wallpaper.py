"""
@Author: Jayce
@FileName: picture.py
@ProjectName: anime_wallpaper
@CreateTime: 2018/7/19 16:13
"""

import os

from srequests import Srequests
from lxml import etree
from urllib.parse import urljoin
from picture import Picture

HOST = 'https://anime-pictures.net'


def get_details_urls(text):
    # 详情
    html = etree.HTML(text)
    etree.cleanup_namespaces()
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
    # srequest = Srequests()
    # if srequest.check_cookies():
    #     pass
    # else:
    #     print('update cookies ！')
    #     loginurl = 'https://anime-pictures.net/login/submit'
    #     logindata = {'login': 'jarvan', 'password': '55223636', 'time_zone': 'Asia/Shanghai'}
    #     srequest.update_cookies(loginurl, logindata)
    #
    # # 获取图片信息
    # taglist = ['girl', 'long hair', 'breasts', 'blush', 'single', 'highres']
    # search_tag = '||'.join(taglist)
    #
    # search_url = "https://anime-pictures.net/pictures/view_posts/0?search_tag=%s&aspect=16:9&order_by=date&ldate=0" \
    #              "&ext_jpg=jpg&ext_png=png&lang=en" % search_tag
    # url2 = 'https://anime-pictures.net/pictures/view_post/558615?lang=en'
    # resp = srequest.session.get(url2, headers=Srequests.headers)
    # print(Srequests.headers)
    # print(print(resp.text))
    #
    # with open('html2', 'w') as handle:
    #     handle.write(resp.content.decode('utf-8'))
    # exit()

    with open('html', 'r') as handle:
        text = handle.read()
    print(get_page_count(text))
    print(get_details_urls(text))

    with open('html2', 'r') as handle:
        text = handle.read()
        # print(text)

    p = Picture(*get_picture_info(text))
    print(p)
