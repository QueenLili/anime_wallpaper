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
    def __init__(self):
        self.db = 'gallery.sqlite3'

    def get_con(self, func):
        data_path = self.db

        def sql_exc(self):
            con = sqlite3.connect(data_path)
            con.text_factory = str
            con.row_factory = dict_factory
            cur = con.cursor()
            func(self, cur)
            con.commit()
            cur.close()
            con.close()

        return sql_exc

    @get_con
    def create_table(self, cur):
        cur.execute('''CREATE TABLE COMPANY
               (ID INT PRIMARY KEY     NOT NULL,
               NAME           TEXT    NOT NULL,
               AGE            INT     NOT NULL,
               ADDRESS        CHAR(50),
               SALARY         REAL);''')


    def save_picture_info(self):
        pass

    def random_picture(self):
        # 从除了不喜欢的图片中随机选取一张图片
        '''SELECT * FROM 表名 ORDER BY RANDOM() limit 1'''
        pass

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
    g.create_table()
