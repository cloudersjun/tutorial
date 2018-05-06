# coding=utf-8
import datetime
import logging
import random
import sys
import time
from random import choice

reload(sys)
sys.setdefaultencoding('utf8')
from scrapy.http import HtmlResponse


def random_ua():
    l = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
         "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
         "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
         "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
         "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
         "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
         "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
         "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
         "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
         "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
         "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
         "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
         "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
         "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
         "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
         "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
         "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
         "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
         "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
         "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]
    return choice(l)


class HandleRequest(object):
    def process_request(self, request, spider):
        # ua = random_ua()
        # if ua:
        #     request.headers.setdefault('User-Agent', ua)
        # request.headers.setdefault('User-Agent', "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36")
        input_item = request.meta["item_info"]
        # request.meta["proxy"] = input_item["proxy"]
        # referer = str(input_item['hotel_url']).split('#')[0]
        # logging.info("referer:" + referer)
        # request.headers.setdefault('Referer', referer)
        spider.driver.get("http://www.baidu.com")
        # spider.driver.navigate().to("http://www.baidu.com")
        time.sleep(2)
        # spider.driver.delete_all_cookies()
        spider.driver.get(request.url)
        # spider.driver.navigate().to(request.url)
        time.sleep(random.randint(1, 3))
        spider.driver.execute_script("scroll(0," + random.randint(580, 600).__str__() + ");")
        now_day = str(datetime.date.today())
        tomorrow = str(datetime.date.today() + datetime.timedelta(days=1))
        # spider.driver.delete_all_cookies()
        if now_day != input_item["start_date"] or tomorrow != input_item["end_date"]:
            self.dom_change(input_item["start_date"], input_item["end_date"], spider.driver)
            spider.driver.find_element_by_xpath("//a[@id='changeBtn']").click()
            time.sleep(random.randint(3, 5))
        time.sleep(2)
        string = spider.driver.page_source
        string = string.decode("utf-8", "ignore").encode("utf-8", "ignore")
        rendered_body = string
        return HtmlResponse(request.url, body=rendered_body, encoding='utf-8')

    def process_response(self, request, response, spider):
        div_dom = response.xpath("//div[@id='hotelRoomBox']").extract()
        # logging.debug("提取到酒店房间数组：{}"+str(div_dom))
        return HtmlResponse(request.url, body=str(div_dom[0]).decode("utf-8", "ignore").encode("utf-8", "ignore"),
                            encoding='utf-8')

    def dom_change(self, start_date, end_date, driver):
        logging.debug(u"操作dom.....")
        time.sleep(random.randint(1, 3))
        start_dom = driver.find_element_by_xpath("//input[@id='cc_txtCheckIn']")
        start_dom.clear()
        start_dom.send_keys(start_date)
        time.sleep(random.randint(1, 3))
        end_dom = driver.find_element_by_xpath("//input[@id='cc_txtCheckOut']")
        end_dom.clear()
        end_dom.send_keys(end_date)
        time.sleep(random.randint(1, 3))
