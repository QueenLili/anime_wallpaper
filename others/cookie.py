"""
@Author: Jayce
@Software: PyCharm
@FileName: srequests.py
@CreateTime: 2018/7/18 23:59
"""
import requests
from requests_toolbelt import MultipartEncoder


class CookieError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


class Cookie(object):
    cookies = None

    def __init__(self):
        self.__loginurl = 'https://anime-pictures.net/login/submit'
        self.__logindata = {'login': 'jarvan', 'password': '55223636', 'time_zone': 'Asia/Shanghai'}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }
        self.update_cookies()

    def update_cookies(self):
        # login
        m = MultipartEncoder(fields=self.__logindata)
        self.headers['Content-Type'] = m.content_type
        rs = requests.post(self.__loginurl, data=m,
                           headers=self.headers, cookies=self.cookies)

        if rs.status_code == 200 and '"success":true' in rs.text:
            # save cookie
            print(rs.text)
            Cookie.cookies = rs.cookies
        else:
            raise CookieError('login error, update cookies failed !')


if __name__ == '__main__':
    Cookie()

    # # s.update_cookies(loginurl, logindata)
    # # print(s.session.get('https://anime-pictures.net/').text)
    # cookic = cookiejar.LWPCookieJar(filename='Cookies')
    # cookic.load(ignore_discard=True)
    print(requests.get('https://anime-pictures.net/', cookies=Cookie.cookies).text)
