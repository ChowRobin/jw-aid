#!/usr/bin/env python

import requests
import re
from time import sleep
import http.cookiejar
from PIL import Image
from bs4 import BeautifulSoup
from urllib import parse
from courseSchedule_Handler import courseSchedule_Handler
from score_Handler import score_Handler
from info_Handler import info_Handler

class Spider:

    def __init__(self):
        # create request headers
        self.Url = 'http://xk1.ahu.cn'
        agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'
        self.postUrl = self.Url + '/default2.aspx'
        self.headers = {
            'Referer': self.postUrl,
            'User-Agent': agent
        }
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

    def login(self, xh, password):
        # create post data
        self.xh = xh
        self.password = password
        RadioButtonList1 = u"学生".encode('gb2312', 'replace')
        res = self.session.get(self.postUrl)
        soup = BeautifulSoup(res.text, 'html.parser')
        viewstate = soup.find('input', id='__VIEWSTATE').get('value')
        eventvalidation = soup.find('input', id='__EVENTVALIDATION').get('value')
        postData = {
            'Button1': '',
            'RadioButtonList1': RadioButtonList1,
            'TextBox2': password,
            '__EVENTVALIDATION': eventvalidation,
            '__VIEWSTATE': viewstate,
            'hidPdrs': '', 
            'hidsc': '',
            'lbLanguage': '',
            'txtSecretCode': self.getCheckCode(),
            'txtUserName': xh
        }
        try:
            loginPage = self.session.post(self.postUrl, data=postData, headers=self.headers)
            self.session.cookies.save()
            self.getInfo()
            print('Login Successful')
        except:
            print('Login failed')

    def getInfo(self):
        infoUrl = self.Url + '/xsgrxx.aspx?xh=' + self.xh + '&'
        self.session.headers['Referer'] = self.Url + '/xs_main.aspx?xh=' + self.xh
        res = self.session.get(infoUrl)
        handler = info_Handler(res.text)
        self.name = handler.getInfo('name')
        self.xm = parse.quote(self.name.encode('gb2312'))

    def getCourseSchedule(self):
        # get Course-Schedule
        csUrl = self.Url + '/xskbcx.aspx?xh=' + self.xh + '&xm=' + self.xm + '&gnmkdm=N121603'
        res = self.session.get(csUrl, headers=self.headers)
        res.encoding = 'gb2312'
        handler = courseSchedule_Handler(res.text)
        handler.writeToFile('course.html')
        print('CourseSchedule has saved as Course.html')        

    def getScore(self):
        # get Score
        scoreUrl = self.Url + '/xscjcx_dq.aspx?xh=' + self.xh
        self.session.headers['Referer'] = scoreUrl
        res = self.session.get(scoreUrl)
        soup = BeautifulSoup(res.text, 'html.parser')
        viewstate = soup.find('input', id='__VIEWSTATE').get('value')
        eventvalidation = soup.find('input', id='__EVENTVALIDATION').get('value')
        postData = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': '',
            '__EVENTVALIDATION': eventvalidation,
            '__LASTFOCUS': '',
            '__VIEWSTATE': viewstate,
            'btnCx': u' 查  询 '.encode('gb2312', 'replace'),
            'ddlxn': u'全部'.encode('gb2312', 'replace'),
            'ddlxq': u'全部'.encode('gb2312', 'replace')
        }
        res = self.session.post(scoreUrl, data=postData, headers=self.headers)
        res.encoding = 'gb2312'
        handler = score_Handler(res.text)
        handler.writeToFile('score.html')
        print("All the score has saved as score.html")

    def getLesson(self, xkurl, id):
        self.session.headers['Referer'] = self.Url + '/xsxk.aspx?xh=' + self.xh + '&xm=%u5468%u6768%u7693' + '&gnmkdm=N121101'
        html = self.session.get(xkurl)
        soup = BeautifulSoup(html.text, 'html.parser')
        viewstate = soup.find('input', id='__VIEWSTATE').get('value')
        eventvalidation = soup.find('input', id='__EVENTVALIDATION').get('value')
        xkkh = soup.find('table', class_='formlist').find_all('tr')[id].find_all('td')[-1].find('input').get('value')
        print(xkkh)
        postData = {
            'RadioButtonList1': '1',
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'Button1',
            '__EVENTVALIDATION': eventvalidation,
            '__VIEWSTATE': viewstate,
            'xkkh': xkkh
        }
        while True:
            sleep(1)
            self.session.headers['Referer'] = xkurl
            res = self.session.post(xkurl, data=postData)
            pattern = re.compile(r".*alert\('([^']+)'\)")
            ans = re.match(pattern, res.text)
            print(ans.group(1))    

def main():
    spider = Spider()
    xh = input('please input xh\n> ')
    password = input('please input password\n> ')
    spider.login(xh, password)
    spider.getCourseSchedule()
    spider.getScore()
    # xkurl = input('please input xkurl\n> ')
    # 从上往下顺序
    # teacherid = input('please input teacherid\n> ')
    # spider.getLesson(xkurl, teacherid)
    

if __name__ == '__main__':
    main()
