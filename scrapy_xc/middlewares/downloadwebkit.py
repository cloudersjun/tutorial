# coding=utf-8
import logging
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')
from scrapy.http import HtmlResponse

# 通过下面的方式进行简单配置输出方式与日志级别
logging.basicConfig(filename='logger.log', level=logging.INFO)


class HandleRequest(object):
    def process_request(self, request, spider):
        print("init browser....")
        spider.driver.get(request.url)
        spider.driver.maximize_window()
        input_item = request.meta["item_info"]
        self.dom_change(input_item["start_date"], input_item["end_date"], spider.driver)
        spider.driver.find_element_by_xpath("//a[@id='changeBtn']").click()
        time.sleep(3)
        string = spider.driver.page_source
        logging.info(type(string))
        string = string.decode("utf-8", "ignore").encode("utf-8", "ignore")
        rendered_body = string
        logging.debug(rendered_body)
        return HtmlResponse(request.url, body=rendered_body, encoding='utf-8')

    def process_response(self, request, response, spider):
        div_dom = response.xpath("//div[@id='hotelRoomBox']").extract()
        logging.debug("提取到酒店房间数组：{}"+str(div_dom))
        return HtmlResponse(request.url, body=str(div_dom[0]).decode("utf-8", "ignore").encode("utf-8", "ignore"),
                            encoding='utf-8')

    def dom_change(self, start_date, end_date, driver):
        start_dom = driver.find_element_by_xpath("//input[@id='cc_txtCheckIn']")
        start_dom.clear()
        start_dom.send_keys(start_date)
        end_dom = driver.find_element_by_xpath("//input[@id='cc_txtCheckOut']")
        end_dom.clear()
        end_dom.send_keys(end_date)
