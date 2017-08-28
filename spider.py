#!/usr/bin/env python

import requests
import http.cookiejar
from PIL import Image
from bs4 import BeautifulSoup
from courseSchedule_Handler import courseSchedule_Handler
from score_Handler import score_Handler

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
        handler = courseSchedule_Handler(res.text)
        handler.writeToFile('course.html')        

    def getScore(self):
        # get Score
        scoreUrl = self.Url + '/xscjcx_dq.aspx?xh=' + self.userid + '&xm=%u5468%u6768%u7693&gnmkdm=N121605'
        self.session.headers['Referer'] = scoreUrl
        resp = self.session.get(scoreUrl)
        #print(resp.content)
        postData = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': '',
            '__EVENTVALIDATION': u'/wEWFwKFoteZAQLGjKL0DQKc6PHxDgKf6O1nApbomfIPApnotegBApjoofIMApvo3egOApLoyfINApXopYsNAprozbADAsCqyt4FAsOqjp8DAsKqkt8CAt2q1h8C3Kq63wMC36r+nwEC3qrCXwLZqobgAQK3jaL0DQLwr8PxAgLxr8PxAgLwksmiDleNuXGqg8zeCMfvDYzr6RTUCoDV'.encode('gb2312', 'replace'),
            '__LASTFOCUS': '',
            '__VIEWSTATE': u'/wEPDwULLTIwMTgzOTA4ODYPFgIeBHRqcXIFATAWAgIBD2QWCAIBDxBkEBUSBuWFqOmDqAkyMDAxLTIwMDIJMjAwMi0yMDAzCTIwMDMtMjAwNAkyMDA0LTIwMDUJMjAwNS0yMDA2CTIwMDYtMjAwNwkyMDA3LTIwMDgJMjAwOC0yMDA5CTIwMDktMjAxMAkyMDEwLTIwMTEJMjAxMS0yMDEyCTIwMTItMjAxMwkyMDEzLTIwMTQJMjAxNC0yMDE1CTIwMTUtMjAxNgkyMDE2LTIwMTcJMjAxNy0yMDE4FRIG5YWo6YOoCTIwMDEtMjAwMgkyMDAyLTIwMDMJMjAwMy0yMDA0CTIwMDQtMjAwNQkyMDA1LTIwMDYJMjAwNi0yMDA3CTIwMDctMjAwOAkyMDA4LTIwMDkJMjAwOS0yMDEwCTIwMTAtMjAxMQkyMDExLTIwMTIJMjAxMi0yMDEzCTIwMTMtMjAxNAkyMDE0LTIwMTUJMjAxNS0yMDE2CTIwMTYtMjAxNwkyMDE3LTIwMTgUKwMSZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnFgECEWQCAw8QZGQWAQIBZAIHD2QWBmYPZBYCZg8WAh4JaW5uZXJodG1sBSUyMDE3LTIwMTjlrablubTnrKwx5a2m5pyf5a2m5Lmg5oiQ57upZAIBD2QWBmYPFgIfAQUS5a2m5Y+377yaRTMxNjE0MDI2ZAIBDxYCHwEFEuWnk+WQje+8muWRqOadqOeak2QCAg8WAh8BBSflrabpmaLvvJrorqHnrpfmnLrnp5HlrabkuI7mioDmnK/lrabpmaJkAgIPZBYEZg8WAh8BBRXkuJPkuJrvvJrnvZHnu5zlt6XnqItkAgEPFgIfAQUd6KGM5pS/54+t77yaMTbnuqfnvZHnu5zlt6XnqItkAgkPPCsACwIADxYIHghEYXRhS2V5cxYAHgtfIUl0ZW1Db3VudGYeCVBhZ2VDb3VudAIBHhVfIURhdGFTb3VyY2VJdGVtQ291bnRmZAE8KwAWARE8KwAEAQAWAh4HVmlzaWJsZWhkZAt2s45v3agDPy/+KoC8AZ3m32G3'.encode('gb2312', 'replace'),
            'btnCx': u' 查  询 '.encode('gb2312', 'replace'),
            'ddlxn': u'全部'.encode('gb2312', 'replace'),
            'ddlxq': u'全部'.encode('gb2312', 'replace')
        }
        res = self.session.post(scoreUrl, data=postData, headers=self.headers)
        res.encoding = 'gb2312'
        handler = score_Handler(res.text)
        handler.writeToFile('score.html')

    def getLesson(self, xkurl, id):
        html = self.session.get(xkurl, headers=headers)
        soup = BeautifulSoup(html.text, 'html.parser')
        print(soup.prettify())
        # viewstate = soup.find('input', name='__VIEWSTATE).get('value')
        # eventvalidation = soup.find('input', name='__EVENTVALIDATION').get('value')
        # xkkh = soup.find('table', class_='formlist').findall('tr')[id].find('td')[-1:].find('input').get('value')
        # print('viewstate:' + viewstate)
        # print('eventvalidation:' + eventvalidation)
        # print('xkkh is' + xkkh)
        postData = {
            'RadioButtonList1': '1',
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'Button1',
            '__EVENTVALIDATION': viewstate.encode('gb2312', 'replace'),
            '__VIEWSTATE': viewstate.encode('gb2312', 'replace'),
            'xkkh': xkkh.encode('gb2312', 'replace')
        }
        self.session.headers['Referer'] = xkurl
        res = self.session.post(xkurl, data=postData)
        #print('res is' + res)    

def main():
    spider = Spider()
    userid= input('please input userid\n> ')
    password = input('please input password\n> ')
    spider.login(userid, password)
    #spider.getCourseSchedule()
    #spider.getScore()
    #spider.getLesson('', 2)

if __name__ == '__main__':
    main()
