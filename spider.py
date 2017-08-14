#!/usr/bin/env python

import requests
import http.cookiejar
from PIL import Image
from bs4 import BeautifulSoup
from courseSchedule_Handler import courseSchedule_Handler

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
        # create post data
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
            #res = loginPage.content
            #soup = BeautifulSoup(res, 'html.parser')
            #print(soup)
            self.session.cookies.save()
            print('Login Successful\n')
        except:
            print('Login failed\n')

    def getCourseSchedule(self):
        # get Course-Schedule
        csUrl = self.Url + '/xskbcx.aspx?xh=' + self.userid + '&xm=%D6%DC%D1%EE%F0%A9&gnmkdm=N121603'
        res = self.session.get(csUrl, headers=self.headers)
        res.encoding = 'gb2312'
        csHandler = courseSchedule_Handler(res.text)
        csHandler.writeToFile()        

    def getScore(self):
        # get Score
        scoreUrl = self.Url + '/xscjcx_dq.aspx?xh=' + self.userid + '&xm=%u5468%u6768%u7693&gnmkdm=N121605'
        self.session.headers['Referer'] = scoreUrl
        f = open('./__VIEWSTATE', 'r')
        __VIEWSTATE = f.read()
        f.close()
        #print(__VIEWSTATE)
        postData = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'ddlxn',
            '__EVENTVALIDATION': '/wEWGQKByZPwAQKOwemfDgLGjKL0DQKc6PHxDgKf6O1nApbomfIPApnotegBApjoofIMApvo3egOApLoyfINApXopYsNAprozbADAsCqyt4FAsOqjp8DAsKqkt8CAt2q1h8C3Kq63wMC36r+nwEC3qrCXwLZqobgAQL/wOmfDgK3jaL0DQLwr8PxAgLxr8PxAgLwksmiDnE+Wy6AljpPvSCDMRc3x0GDPNym',
            '__LASTFOCUS': '',
            '__VIEWSTATE': __VIEWSTATE,
            'ddlxn': 'È«²¿',
            'ddlxq': 'È«²¿'
        }
        res = self.session.post(scoreUrl, data=postData)
        print(res.text)

def main():
    spider = Spider()
    userid= input('please input userid\n> ')
    password = input('please input password\n> ')
    spider.login(userid, password)
    #spider.getCourseSchedule()
    #spider.getScore()

if __name__ == '__main__':
    main()
