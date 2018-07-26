"""
@Author: Jayce
@Software: PyCharm
@FileName: gallery.py
@CreateTime: 2018/7/20 19:30
"""

import os
import sqlite3
import traceback

import requests

from picture import Picture


def mark_downloaded_tag(pic: Picture, tag: str):
    # '0':no download '1':downloaded
    conn = sqlite3.connect(Gallery.DB)
    with conn:
        conn.execute(
            '''UPDATE gallery SET file_exist = ? WHERE url = ?''', (tag, pic.url))
        conn.commit()
    pic.file_exist = tag


def mark_like_tag(pic: Picture, tag: str):
    # '1':like '0':unlike '':no tag
    conn = sqlite3.connect(Gallery.DB)
    with conn:
        conn.execute(
            '''UPDATE gallery SET islike = ? WHERE url = ?''', (tag, pic.url))
        conn.commit()
    pic.islike = tag


def random_picture():
    # 从除了不喜欢的图片中随机选取一张图片
    '''SELECT * FROM 表名 ORDER BY RANDOM() limit 1'''
    conn = sqlite3.connect(Gallery.DB)
    with conn:
        result = conn.execute(
            '''SELECT url, file_size, resolution_ratio, release_date, file_name, file_path, file_exist, islike, create_date FROM gallery WHERE islike!="0" ORDER BY RANDOM() limit 1''')
        for row in result:
            return Picture(*row)


def save_picture_info(pic: Picture):
    try:
        conn = sqlite3.connect(Gallery.DB)
        with conn:
            conn.execute('''INSERT INTO gallery (url, file_size, resolution_ratio, release_date, file_name, file_path, file_exist, islike, create_date) \
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                         (pic.url, pic.file_size, pic.resolution_ratio, pic.release_date,
                          pic.file_name, pic.file_path, pic.file_exist, pic.islike, pic.create_date))
            conn.commit()
            print('saved...')
    except sqlite3.IntegrityError as e:
        print('已存在。')


def get_pictures_count():
    '''SELECT count(*) FROM gallery;'''
    conn = sqlite3.connect(Gallery.DB)
    with conn:
        result = conn.execute('''SELECT count(*) FROM gallery;''')
        for i in result:
            return i[0]


def del_picture(pic: Picture):
    try:
        os.remove(pic.file_path)
        mark_downloaded_tag(pic, '0')
    except:
        traceback.print_exc()


def download_picture(pic: Picture):
    if os.path.exists(pic.file_path) and pic.file_exist == '1':
        return True
    try:
        data = requests.get(pic.url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}).content
    except Exception as e:
        print(e)
        return False
    with open(pic.file_path, 'wb') as handle:
        handle.write(data)
    mark_downloaded_tag(pic, '1')
    return True


class Gallery(object):
    DB = 'gallery.db'

    def __init__(self):
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(Gallery.DB)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS  gallery
                       (ID               INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                       url               TEXT UNIQUE,
                       file_name         TEXT,
                       file_path         TEXT,
                       file_exist        CHAR(1),
                       islike            CHAR(1),
                       file_size         CHAR(20),
                       resolution_ratio  CHAR(20),
                       release_date      CHAR(20),
                       create_date       CHAR(20));''')
            conn.execute('''CREATE INDEX IF NOT EXISTS islike_index ON gallery (islike);''')
            conn.commit()


if __name__ == '__main__':
    g = Gallery()
    get_pictures_count()
    a = Picture(
        'https://anime-pictures.net/pictures/get_image/278381-1920x1080-berry%26%2339%3Bs-morikubo+yuna-suzuhira+hiro-long+hair-blush-highres.png',
        '2.9MB', '1920x1080', '6/14/18, 3:49 PM')
    print(a)
    save_picture_info(a)
    pic = random_picture()
    print(pic, '==============================')
    download_picture(pic)
    print(pic)
    mark_like_tag(pic, '1')
    print(pic)
