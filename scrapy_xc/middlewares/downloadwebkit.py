# coding=utf-8
import pyquery
import time
import BeautifulSoup
import sys
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
from selenium.webdriver.common.keys import Keys #引入keys类操作
from chardet import detect


class HandleRequest( object ):
    def __init__(self):
        print("init browser....")
        # self.driver = webdriver.PhantomJS()
        # time.sleep(5)
        self.driver = webdriver.PhantomJS(executable_path="phantomjs.exe")

    def process_request( self, request, spider ):
        self.driver.get(request.url)
        print '现在将浏览器最大化'
        self.driver.maximize_window()
        time.sleep(3)
        string = self.driver.page_source
        # 编码处
        coding = detect(string)['encoding']
        print('coding: {}'.format(coding))
        print('content: {}'.format(string.decode(coding).rstrip()))
        print string
        renderedBody = str(string)
        return HtmlResponse( request.url, body=renderedBody,encoding='utf-8' )
    def  spider_closed(self):
        print("close driver....")
        self.driver.close()