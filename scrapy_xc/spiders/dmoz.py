# -*- coding: utf-8 -*-
import logging
import sys
from datetime import datetime, timedelta
import time

from scrapy_xc import settings
from scrapy_xc.handle_input import HandleInput
from scrapy_xc.handle_output import HandleOutput
from scrapy_xc.handler_parse import HandleParse

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import scrapy.utils.project
import scrapy.utils.engine
import scrapy.utils.template
import scrapy.utils.python
import scrapy.utils.deprecate
import scrapy.spiderloader
import scrapy.statscollectors
import scrapy.logformatter
import scrapy.extensions.closespider
import scrapy.extensions.feedexport
import scrapy.extensions.memdebug
import scrapy.extensions.memusage
import scrapy.extensions.logstats
import scrapy.extensions.telnet
import scrapy.extensions.corestats
import scrapy.extensions.spiderstate
import scrapy.extensions.throttle
import scrapy.extensions.debug
import scrapy.extensions.httpcache
import scrapy.extensions.statsmailer
import scrapy.core.scheduler
import scrapy.core.downloader
import scrapy.core.engine
import scrapy.core.scraper
import scrapy.core.spidermw
import scrapy.downloadermiddlewares.robotstxt
import scrapy.downloadermiddlewares.retry
import scrapy.downloadermiddlewares.stats
import scrapy.downloadermiddlewares.cookies
import scrapy.downloadermiddlewares.decompression
import scrapy.downloadermiddlewares.httpauth
import scrapy.downloadermiddlewares.httpproxy
import scrapy.downloadermiddlewares.downloadtimeout
import scrapy.downloadermiddlewares.defaultheaders
import scrapy.downloadermiddlewares.httpcache
import scrapy.downloadermiddlewares.ajaxcrawl
import scrapy.downloadermiddlewares.useragent
import scrapy.downloadermiddlewares.redirect
import scrapy.downloadermiddlewares.httpcompression
import scrapy.spidermiddlewares.httperror
import scrapy.spidermiddlewares.depth
import scrapy.spidermiddlewares.offsite
import scrapy.spidermiddlewares.referer
import scrapy.spidermiddlewares.urllength
import scrapy.pipelines
import scrapy.dupefilters
import scrapy.squeues
import scrapy.core.downloader.handlers.http
import scrapy.core.downloader.contextfactory
import scrapy.core.downloader.middleware
import scrapy.utils.conf
import scrapy.exceptions
import scrapy_xc.spiders
import scrapy_xc.middlewares.downloadwebkit


# 通过下面的方式进行简单配置输出方式与日志级别
logging.basicConfig(filename='logger.log', level=logging.INFO)

reload(sys)
sys.setdefaultencoding('utf8')


class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    file_path = "./"
    logging.info('start init....')
    file_name = "result.xlsx"
    handle_input = HandleInput()
    # {"name":，"room_type":,"price_dic":{"date":,"price":}]}
    global out_map
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
    driver = webdriver.Chrome(executable_path="chromedriver.exe",
                              chrome_options=chrome_options)

    # driver.maximize_window()
    input_array = handle_input.ret_array

    def start_requests(self):
        #logging.info(len(self.input_array))
        #logging.debug(self.input_array)
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
        #logging.debug(input_item)
        # with open(input_item["name"] + "_" + input_item["start_date"] + "_" + input_item["end_date"] + ".html",
        #           'w') as f:
        #     f.write(response.body)
        parse = HandleParse(response,datetime.strptime(input_item["start_date"], "%Y-%m-%d"),datetime.strptime(input_item["end_date"], "%Y-%m-%d"),input_item["room_type"],input_item["name"])
        parse.parse(out_map)

    def close(self, reason):
        logging.info('close driver......')
        self.driver.close()
        temp_date = self.min_date
        while temp_date < self.max_date:
            self.file_header.append(temp_date.strftime("%Y-%m-%d"))
            temp_date += timedelta(days=1)
        logging.debug(u"解析结果dic:"+str(out_map))
        handle_output = HandleOutput(self.file_path, self.file_name, self.file_header, out_map,
                                     self.input_array)
        handle_output.write()

settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(DmozSpider)
process.start()