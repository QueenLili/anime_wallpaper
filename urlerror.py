# -*- coding: UTF-8 -*-
from urllib import request
# from urllib import error
import urllib
if __name__ == "__main__":
    #一个不存在的连接
    url = "http://www.iloakjdfkjdfveyou.com/"
    req = request.Request(url)
    try:
        response = request.urlopen(req)
        html = response.read().decode('utf-8')
        print(html)
    except urllib.error.URLError as e:
        print(e.reason)