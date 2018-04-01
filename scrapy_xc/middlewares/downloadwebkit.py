# coding=utf-8
import pyquery
import time
import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains  # 引入ActionChains鼠标操作类
from selenium.webdriver.common.keys import Keys  # 引入keys类操作
from chardet import detect
from scrapy.conf import settings


class HandleRequest(object):
    def __init__(self):
        print("init browser....")
        # self.driver = webdriver.PhantomJS()
        # time.sleep(5)
        self.driver = webdriver.PhantomJS(executable_path="phantomjs.exe")

    def process_request(self, request, spider):
        self.driver.get(request.url)
        self.driver.maximize_window()
        self.dom_change(request["start_date"], request["end_date"])
        self.driver.find_element_by_xpath("//a[@id='changeBtn']").click()
        print u'现在将浏览器最大化'
        time.sleep(3)
        string = self.driver.page_source
        # 编码处
        print type(string)
        string = string.decode("utf-8", "ignore").encode("utf-8", "ignore")
        renderedBody = string
        if settings["DEBUG"]:
            print(renderedBody)
        return HtmlResponse(request.url, body=renderedBody, encoding='utf-8')

    def spider_closed(self):
        print("close driver....")
        self.driver.close()

    def dom_change(self, start_date, end_date):
        start_dom = self.driver.find_element_by_xpath("//input[@id='cc_txtCheckIn']")
        start_dom.clear()
        start_dom.send_keys(start_date)
        end_dom = self.driver.find_element_by_xpath("//input[@id='cc_txtCheckOut']")
        end_dom.clear()
        self.keys = end_dom.send_keys(end_date)
