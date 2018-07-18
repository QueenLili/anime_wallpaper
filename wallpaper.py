from srequests import Srequests

if __name__ == '__main__':
    srequest = Srequests()
    if srequest.check_cookies():
        pass
    else:
        print('update cookies ！')
        loginurl = 'https://anime-pictures.net/login/submit'
        logindata = {'login': 'xxx', 'password': 'xxx', 'time_zone': 'Asia/Shanghai'}
        srequest.update_cookies(loginurl, logindata)

    # 获取首页信息
    home_url = "https://anime-pictures.net/pictures/view_posts/0?search_tag=girl%7Clong%20hair%7C%7Cbreasts&aspect=16%3A9&order_by=date&ldate=0&ext_jpg=jpg&ext_png=png&lang=en"
    resp = srequest.session.get(home_url, headers=Srequests.headers, allow_redirects=False)
    print(Srequests.headers)
    # print(resp.text)
