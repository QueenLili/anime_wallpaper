"""
@Author: Jayce
@FileName: picture.py
@ProjectName: anime_wallpaper
@CreateTime: 2018/7/19 16:13
"""

import os
import time


class Picture(object):
    DOWNLOAD_DIR = 'Gallery'

    def __init__(self, url, release_date, resolution_ratio, file_size):
        self.url = url
        self.file_name = os.path.basename(url)
        self.file_path = os.path.join(Picture.DOWNLOAD_DIR, self.file_name)
        self.like = ''
        self.file_size = file_size
        self.resolution_ratio = resolution_ratio
        self.release_date = time.strftime("%Y-%m-%d %H:%M", time.strptime(release_date, '%m/%d/%y, %I:%M %p'))
        self.create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def __str__(self):
        return 'url: %s, file_name: %s, file_path: %s, file_size: %s, like: %s, resolution_ratio: %s, release_date: %s, create_date: %s' % (
            self.url, self.file_name, self.file_path, self.file_size, self.like, self.resolution_ratio,
            self.release_date, self.create_date)


if __name__ == '__main__':
    a = Picture('http://www.xxx.com/asdf.jpg', '6/14/18, 3:49 PM', '1920x1080', '2.9MB')
    print(a)
