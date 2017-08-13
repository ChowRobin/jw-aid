#!/usr/bin/env python

import requests
import http.cookiejar
from PIL import Image
from bs4 import BeautifulSoup

class loginSpider:

    def __init__(self):
        # create request headers
        agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'
        self.headers = {
            'Referer': 'http://xk1.ahu.cn/default2.aspx',
            'User-Agent': agent
        }

        self.postUrl = 'http://xk1.ahu.cn/default2.aspx'
        self.session = requests.session()
        self.session.cookies = http.cookiejar.LWPCookieJar(filename='cookie')

    def loadCookie(self):
        pass

    def getCheckCode(self):
        imgUrl = 'http://xk1.ahu.cn/CheckCode.aspx'
        img = self.session.get(imgUrl)

        with open('./checkCode.jpg', 'wb') as f:
            f.write(img.content)
        cc = Image.open('./checkCode.jpg')
        cc.show()
        code = input('please input the checkcode\n> ')
        cc.close()
        return code

    def Login(self, username, password):
        #create post data
        RadioButtonList1 = u"学生".encode('gb2312', 'replace')
        postData = {
            'Button1': '',
            'RadioButtonList1': RadioButtonList1,
            'TextBox2': password,
            '__EVENTVALIDATION': '/wEWDgKX/4yyDQKl1bKzCQLs0fbZDAKEs66uBwK/wuqQDgKAqenNDQLN7c0VAuaMg+INAveMotMNAoznisYGArursYYIAt+RzN8IApObsvIHArWNqOoPqeRyuQR+OEZezxvi70FKdYMjxzk=',
            '__VIEWSTATE': '/wEPDwUJODk4OTczODQxZGQhFC7x2TzAGZQfpidAZYYjo/LeoQ==',
            'hidPdrs': '', 
            'hidsc': '',
            'lbLanguage': '',
            'txtSecretCode': self.getCheckCode(),
            'txtUserName': username
        }
        try:
            loginPage = self.session.post(self.postUrl, data=postData, headers=self.headers)
            res = loginPage.content
            soup = BeautifulSoup(res, 'html.parser')
            print(soup)
            self.session.cookies.save()
        except:
            print('Login failed\n')

def main():
    spider = loginSpider()
    username = input('please input username\n> ')
    password = input('please input password\n> ')
    spider.Login(username, password)

if __name__ == '__main__':
    main()
