# -*- coding: utf-8 -*-
import logging
import sys
from datetime import datetime, timedelta

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scrapy_xc.handle_input import HandleInput
from scrapy_xc.handle_output import HandleOutput
from scrapy_xc.handler_parse import HandleParse

# 通过下面的方式进行简单配置输出方式与日志级别
logging.basicConfig(filename='logger.log', level=logging.INFO)

reload(sys)
sys.setdefaultencoding('utf8')


class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    # allowed_domains = ['dmoz.org']
    # start_urls = ["http://hotels.ctrip.com/hotel/396401.html#ctm_ref=hod_dl_map_ htllst_n_9"]
    print('start init....')
    file_path = "./"
    file_name = "result.xls"
    logging.info('start init....')
    file_path = "/Users/yujun/gitPro/tutorial/"
    file_name = "result.xlsx"
    handle_input = HandleInput()
    # {"name":，"room_type":,"price_dic":{"date":,"price":}]}
    out_map = {}
    file_header = ["name", "room_type"]
    max_date = None
    min_date = None
    logging.info("init browser....")
    chrome_options = Options()
    # chrome_options.set_headless(True)
    # 不加载图片
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path="/Users/yujun/gitPro/tutorial/chromedriver",
                              chrome_options=chrome_options)
    input_array = handle_input.ret_array

    def start_requests(self):
        logging.info(len(self.input_array))
        logging.debug(self.input_array)
        for input_item in self.input_array:
            logging.info(input_item)
            if self.min_date is None or self.min_date > datetime.strptime(input_item["start_date"], "%Y-%m-%d"):
                self.min_date = datetime.strptime(input_item["start_date"], "%Y-%m-%d")
            if self.max_date is None or self.max_date < datetime.strptime(input_item["end_date"], "%Y-%m-%d"):
                self.max_date = datetime.strptime(input_item["end_date"], "%Y-%m-%d")
            request = scrapy.Request(url=input_item["hotel_url"], callback=self.parse, dont_filter=True)
            request.meta["item_info"] = input_item
            yield request

    def parse(self, response):
        input_item = response.meta["item_info"]
        logging.debug(input_item)
        with open(input_item["name"] + "_" + input_item["start_date"] + "_" + input_item["end_date"] + ".html",
                  'w') as f:
            f.write(response.body)
        parse = HandleParse(response,datetime.strptime(input_item["start_date"], "%Y-%m-%d"),datetime.strptime(input_item["end_date"], "%Y-%m-%d"),input_item["name"],input_item["room_type"])
        parse.parse(self.out_map)

    def close(self, reason):
        logging.info('close driver......')
        self.driver.close()
        temp_date = self.min_date
        while temp_date <= self.max_date:
            self.file_header.append(temp_date.strftime("%Y-%m-%d"))
            temp_date += timedelta(days=1)

        logging.debug(self.out_map)
        handle_output = HandleOutput(self.file_path, self.file_name, self.file_header, self.out_map,
                                     self.input_array)
        handle_output.write()
