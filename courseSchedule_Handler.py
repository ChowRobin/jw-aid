#!/usr/bin/env python

import re
from bs4 import BeautifulSoup

class courseSchedule_Handler:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.table = self.soup.find('table', class_='blacktab')
    
    def writeToFile(self, filename):
        with open(filename, 'w') as f:
            f.write('<html lang=\'gb2312\'><head><title>课表</title><meta content="text/html; charset=utf-8" http-equiv="Content-Type"><meta content=\"gb2312\" http-equiv=\"Content-Language\"></head><body>')
            f.write(str(self.table))
            f.write('</body></html>')
