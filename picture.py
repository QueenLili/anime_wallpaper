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

    def __init__(self, url, file_size, resolution_ratio, release_date, file_name=None, file_path=None, file_exist=None, islike=None, create_date=None):
        self.url = url
        self.file_size = file_size
        self.resolution_ratio = resolution_ratio
        if ',' in release_date:
            self.release_date = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(release_date, '%m/%d/%y, %I:%M %p'))
        else:
            self.release_date = release_date
        if file_name is None:
            self.file_name = os.path.basename(url)
        else:
            self.file_name = file_name
        if file_path is None:
            self.file_path = os.path.join(Picture.DOWNLOAD_DIR, self.file_name)
        else:
            self.file_path = file_path
        if file_exist is None:
            self.file_exist = ''
        else:
            self.file_exist = file_exist
        if islike is None:
            self.islike = ''
        else:
            self.islike = islike
        if create_date is None:
            self.create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        else:
            self.create_date = create_date

    def __str__(self):
        return 'url: %s, file_name: %s, file_path: %s, file_size: %s, like: %s, resolution_ratio: %s, release_date: %s, create_date: %s' % (
            self.url, self.file_name, self.file_path, self.file_size, self.islike, self.resolution_ratio,
            self.release_date, self.create_date)


if __name__ == '__main__':
    a = Picture('http://www.xxx.com/asdf.jpg', '2.9MB', '1920x1080', '6/14/18, 3:49 PM')
    print(a)
