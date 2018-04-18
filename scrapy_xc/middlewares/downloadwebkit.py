# coding=utf-8
import logging
import sys
import time
from random import Random, random

from scrapy.conf import settings

reload(sys)
sys.setdefaultencoding('utf8')
from scrapy.http import HtmlResponse


class HandleRequest(object):
    def process_request(self, request, spider):
        ua = random.choice(settings.get('USER_AGENT_LIST'))
        if ua:
            request.headers.setdefault('User-Agent', ua)
        input_item = request.meta["item_info"]
        referer = str(input_item['hotel_url']).split('#')[0]
        logging.info("referer:" + referer)
        request.headers.setdefault('Referer', referer)
        spider.driver.get(request.url)
        self.dom_change(input_item["start_date"], input_item["end_date"], spider.driver)
        spider.driver.find_element_by_xpath("//a[@id='changeBtn']").click()
        time.sleep(Random.randint(1, 3))
        spider.driver.refresh()
        spider.driver.execute_script("scroll(0," + Random.randint(590, 650).__str__() + ");")
        spider.driver.find_element_by_xpath("//a[@id='changeBtn']").click()
        time.sleep(Random.randint(3, 5))
        string = spider.driver.page_source
        # logging.info(type(string))
        string = string.decode("utf-8", "ignore").encode("utf-8", "ignore")
        rendered_body = string
        # logging.debug(rendered_body)
        return HtmlResponse(request.url, body=rendered_body, encoding='utf-8')

    def process_response(self, request, response, spider):
        div_dom = response.xpath("//div[@id='hotelRoomBox']").extract()
        # logging.debug("提取到酒店房间数组：{}"+str(div_dom))
        return HtmlResponse(request.url, body=str(div_dom[0]).decode("utf-8", "ignore").encode("utf-8", "ignore"),
                            encoding='utf-8')

    def dom_change(self, start_date, end_date, driver):
        logging.debug(u"操作dom.....")
        start_dom = driver.find_element_by_xpath("//input[@id='cc_txtCheckIn']")
        start_dom.clear()
        start_dom.send_keys(start_date)
        end_dom = driver.find_element_by_xpath("//input[@id='cc_txtCheckOut']")
        end_dom.clear()
        end_dom.send_keys(end_date)
