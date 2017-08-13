#!/usr/bin/env python

import requests
import http.cookiejar
from PIL import Image
from bs4 import BeautifulSoup

class Spider:

    def __init__(self):
        # create request headers
        agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'
        self.headers = {
            'Referer': 'http://xk1.ahu.cn/default2.aspx',
            'User-Agent': agent
        }
        self.Url = 'http://xk1.ahu.cn'
        self.postUrl = self.Url + '/default2.aspx'
        self.session = requests.session()
        self.session.cookies = http.cookiejar.LWPCookieJar(filename='cookie')

    def getCheckCode(self):
        imgUrl = self.Url + '/CheckCode.aspx'
        img = self.session.get(imgUrl)

        with open('./checkCode.jpg', 'wb') as f:
            f.write(img.content)
        cc = Image.open('./checkCode.jpg')
        cc.show()
        code = input('please input the checkcode\n> ')
        cc.close()
        return code

    def login(self, userid, password):
        #create post data
        self.userid = userid
        self.password = password
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
            'txtUserName': userid
        }
        try:
            loginPage = self.session.post(self.postUrl, data=postData, headers=self.headers)
#            res = loginPage.content
#            soup = BeautifulSoup(res, 'html.parser')
#            print(soup)
            self.session.cookies.save()
            print('Login Successful\n')
        except:
            print('Login failed\n')

    def getCourseSchedule(self):
        #get Course-Schedule
        csUrl = self.Url + '/xskbcx.aspx?xh=' + self.userid + '&xm=%D6%DC%D1%EE%F0%A9&gnmkdm=N121603'
        res = self.session.get(csUrl, headers=self.headers)
        print(res.text)

def main():
    spider = Spider()
    username = input('please input username\n> ')
    password = input('please input password\n> ')
    spider.login(username, password)
    spider.getCourseSchedule()

if __name__ == '__main__':
    main()
