"""
@Author: Jayce
@Software: PyCharm
@FileName: gallery.py
@CreateTime: 2018/7/20 19:30
"""

import sqlite3

import requests

from picture import Picture


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Gallery(object):
    db = 'gallery.db'

    def __init__(self):
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(Gallery.db)
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
            print("table created")

    def save_picture_info(self, pic: Picture):
        try:
            conn = sqlite3.connect(Gallery.db)
            with conn:
                conn.execute('''INSERT INTO gallery (url, file_size, resolution_ratio, release_date, file_name, file_path, file_exist, islike, create_date) \
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                             (pic.url, pic.file_size, pic.resolution_ratio, pic.release_date,
                              pic.file_name, pic.file_path, pic.file_exist, pic.islike, pic.create_date))
                conn.execute('''create index islike_index on gallery (islike);''')
        except sqlite3.IntegrityError as e:
            print(e)

    def random_picture(self):
        # 从除了不喜欢的图片中随机选取一张图片
        '''SELECT * FROM 表名 ORDER BY RANDOM() limit 1'''
        conn = sqlite3.connect(Gallery.db)
        with conn:
            result = conn.execute(
                '''SELECT url, file_size, resolution_ratio, release_date, file_name, file_path, file_exist, islike, create_date FROM gallery WHERE islike!="0" ORDER BY RANDOM() limit 1''')
            for row in result:
                return Picture(*row)

    def mark_like_tag(self, pic: Picture, tag: bool):
        # '1':like '0':unlike '':no tag
        pass

    def mark_downloaded_tag(self, pic: Picture, tag: bool):
        # '0':no download '1':downloaded
        pass

    def del_picture(self, pic: Picture):
        pass
        self.mark_downloaded_tag(pic, False)

    def download_picture(self, pic: Picture):
        try:
            data = requests.get(pic.url)
        except Exception as e:
            print(e)
            return False
        with open(pic.file_path, 'wb') as handle:
            handle.write(data.content)
        self.mark_downloaded_tag(pic, True)
        return True


if __name__ == '__main__':
    g = Gallery()
    a = Picture('http://www.xxx.com/asdf.jpg', '2.9MB', '1920x1080', '6/14/18, 3:49 PM')
    print(a)
    g.save_picture_info(a)
    pic = g.random_picture()
    print(pic)

