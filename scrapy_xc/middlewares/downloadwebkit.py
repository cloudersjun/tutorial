# coding=utf-8
import datetime
import logging
import random
import sys
import time
from random import choice
import ConfigParser

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


def click(driver):
    driver.find_element_by_xpath("//a[@id='changeBtn']").click()
    # script = "var a =window['document']['$cdc_asdjflasutopfhvcZLmcfl_'];window['document']['$cdc_asdjflasutopfhvcZLmcfl_']=null;" \
    #          "var now = new Date();var exitTime = now.getTime() + 11*1000; " \
    #          "while (true) { now = new Date(); if (now.getTime() > exitTime){ window['document'][" \
    #          "'$cdc_asdjflasutopfhvcZLmcfl_']=a;break}}; "
    # logging.info(script)
    # driver.execute_script(script)
    # driver.execute_script("window['document']['$cdc_asdjflas' + 'utopfhvcZLmcfl_']=null")
    # driver.execute_script("alert(a)")


def dom_change(start_date, end_date, driver):
    logging.debug(u"操作dom.....")
    start_dom = driver.find_element_by_xpath("//input[@id='cc_txtCheckIn']")
    start_dom.clear()
    start_dom.send_keys(start_date)
    end_dom = driver.find_element_by_xpath("//input[@id='cc_txtCheckOut']")
    end_dom.clear()
    end_dom.send_keys(end_date)


class HandleRequest(object):
    def process_request(self, request, spider):
        input_item = request.meta["item_info"]
        spider.driver.get(request.url)
        seconds_kv = self.getRandomSeconds()
        time.sleep(random.randint(int(seconds_kv["start"]), int(seconds_kv["end"])))
        spider.driver.execute_script("scroll(0," + random.randint(580, 600).__str__() + ");")
        now_day = str(datetime.date.today())
        tomorrow = str(datetime.date.today() + datetime.timedelta(days=1))
        # spider.driver.delete_all_cookies()
        if now_day != input_item["start_date"] or tomorrow != input_item["end_date"]:
            dom_change(input_item["start_date"], input_item["end_date"], spider.driver)
            click(spider.driver)
            time.sleep(random.randint(int(seconds_kv["start"]), int(seconds_kv["end"])))
        string = spider.driver.page_source
        string = string.decode("utf-8", "ignore").encode("utf-8", "ignore")
        rendered_body = string
        return HtmlResponse(request.url, body=rendered_body, encoding='utf-8')

    def process_response(self, request, response, spider):
        div_dom = response.xpath("//div[@id='hotelRoomBox']").extract()
        # logging.debug("提取到酒店房间数组：{}"+str(div_dom))
        return HtmlResponse(request.url, body=str(div_dom[0]).decode("utf-8", "ignore").encode("utf-8", "ignore"),
                            encoding='utf-8')

    def getRandomSeconds(self):
        conf = ConfigParser.ConfigParser()
        conf.read("settings.ini")
        kv = {}
        kv["start"] = conf.get("random_seconds","start")
        kv["end"] = conf.get("random_seconds","end")
        return kv
