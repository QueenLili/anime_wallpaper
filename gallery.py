"""
@Author: Jayce
@Software: PyCharm
@FileName: gallery.py
@CreateTime: 2018/7/20 19:30
"""

import sqlite3
import traceback
import requests
import os

from picture import Picture


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

            print("table created")

    def save_picture_info(self, pic: Picture):
        try:
            conn = sqlite3.connect(Gallery.DB)
            with conn:
                conn.execute('''INSERT INTO gallery (url, file_size, resolution_ratio, release_date, file_name, file_path, file_exist, islike, create_date) \
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                             (pic.url, pic.file_size, pic.resolution_ratio, pic.release_date,
                              pic.file_name, pic.file_path, pic.file_exist, pic.islike, pic.create_date))
        except sqlite3.IntegrityError as e:
            print(e)

    def random_picture(self):
        # 从除了不喜欢的图片中随机选取一张图片
        '''SELECT * FROM 表名 ORDER BY RANDOM() limit 1'''
        conn = sqlite3.connect(Gallery.DB)
        with conn:
            result = conn.execute(
                '''SELECT url, file_size, resolution_ratio, release_date, file_name, file_path, file_exist, islike, create_date FROM gallery WHERE islike!="0" ORDER BY RANDOM() limit 1''')
            for row in result:
                return Picture(*row)

    def mark_like_tag(self, pic: Picture, tag: str):
        # '1':like '0':unlike '':no tag
        conn = sqlite3.connect(Gallery.DB)
        with conn:
            conn.execute(
                '''UPDATE gallery SET islike = ? WHERE url = ?''', (tag, pic.url))
        pic.islike = tag

    def mark_downloaded_tag(self, pic: Picture, tag: str):
        # '0':no download '1':downloaded
        conn = sqlite3.connect(Gallery.DB)
        with conn:
            conn.execute(
                '''UPDATE gallery SET file_exist = ? WHERE url = ?''', (tag, pic.url))
        pic.file_exist = tag

    def del_picture(self, pic: Picture):
        try:
            os.remove(pic.file_path)
            self.mark_downloaded_tag(pic, '0')
        except:
            traceback.print_exc()

    def download_picture(self, pic: Picture):
        if os.path.exists(pic.file_path) and pic.file_exist == '1':
            return True
        try:
            data = requests.get(pic.url)
        except Exception as e:
            print(e)
            return False
        with open(pic.file_path, 'wb') as handle:
            handle.write(data.content)
        self.mark_downloaded_tag(pic, '1')
        return True


if __name__ == '__main__':
    g = Gallery()
    a = Picture('https://anime-pictures.net/pictures/get_image/278381-1920x1080-berry%26%2339%3Bs-morikubo+yuna-suzuhira+hiro-long+hair-blush-highres.png', '2.9MB', '1920x1080', '6/14/18, 3:49 PM')
    print(a)
    g.save_picture_info(a)
    pic = g.random_picture()
    print(pic, '==============================')
    g.download_picture(pic)
    print(pic)
    g.mark_like_tag(pic, '1')
    print(pic)
    g.del_picture(pic)
    print(pic)
