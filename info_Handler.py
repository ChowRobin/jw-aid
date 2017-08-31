#!/usr/bin/env python
from bs4 import BeautifulSoup

class info_Handler:
    
    def __init__(self, html):
        self.Info = {}
        soup = BeautifulSoup(html, 'html.parser')
        self.Info['name'] = soup.find('table', 'formlist').find_all('tr')[1].find_all('td')[1].find('span').text
        
    def getInfo(self, Attr):
        return self.Info[Attr]
        
    