# encoding: utf-8

"""
@Author: Mr. Li
@Software: PyCharm
@FileName: srequests.py
@CreateTime: 2018/7/18 23:59
"""
from http import cookiejar

import grequests
from requests_toolbelt import MultipartEncoder


class SrequestsError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


class Srequests:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }

    def __init__(self):
        self.header = Srequests.headers
        self.session = grequests.Session()
        self.session.cookies = cookiejar.LWPCookieJar(filename='Cookies')

    def check_cookies(self):
        try:
            # load Cookies file
            self.session.cookies.load(ignore_discard=True)
            print(self.session.cookies)
            return True
        except:
            return False

    def update_cookies(self, loginurl, postdata):
        # login
        m = MultipartEncoder(fields=postdata)
        self.header['Content-Type'] = m.content_type
        rs = self.session.post(loginurl, data=m,
                               headers=self.header)
        if rs.status_code == 200 and '"success":true' in rs.text:
            # save cookie
            print(rs.text)
            self.session.cookies.save()
        else:
            raise SrequestsError('login error, update cookies failed !')

    def close(self):
        self.session.close()

if __name__ == '__main__':
    s = Srequests()
    s.close()
