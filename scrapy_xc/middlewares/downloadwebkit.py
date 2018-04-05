# coding=utf-8
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')
from scrapy.http import HtmlResponse
from selenium import webdriver
from scrapy.conf import settings


class HandleRequest(object):
    def __init__(self):
        diver = None
        pass

    def process_request(self, request, spider):
        print("init browser....")
        self.driver = webdriver.Chrome(executable_path="/Users/liukaizhao/tutorial/chromedriver")
        self.driver.get(request.url)
        self.driver.maximize_window()
        input_item = request.meta["item_info"]
        self.dom_change(input_item["start_date"], input_item["end_date"])
        self.driver.find_element_by_xpath("//a[@id='changeBtn']").click()
        time.sleep(3)
        string = self.driver.page_source
        # 编码处
        print type(string)
        string = string.decode("utf-8", "ignore").encode("utf-8", "ignore")
        rendered_body = string
        if settings["DEBUG"]:
            print(rendered_body)
        return HtmlResponse(request.url, body=rendered_body, encoding='utf-8')

    def process_response(self, request, response, spider):
        div_dom = response.xpath("//div[@id='hotelRoomBox']").extract()
        print ('close driver......')
        self.driver.close()
        return HtmlResponse(request.url, body=str(div_dom[0]).decode("utf-8", "ignore").encode("utf-8", "ignore"),
                            encoding='utf-8')

    def dom_change(self, start_date, end_date):
        start_dom = self.driver.find_element_by_xpath("//input[@id='cc_txtCheckIn']")
        start_dom.clear()
        start_dom.send_keys(start_date)
        end_dom = self.driver.find_element_by_xpath("//input[@id='cc_txtCheckOut']")
        end_dom.clear()
        end_dom.send_keys(end_date)
