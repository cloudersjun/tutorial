# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime, timedelta

import sys
from random import Random, random

from scrapy_xc import settings
from scrapy_xc.handle_input import HandleInput
from scrapy_xc.handle_ip import Handle_ip
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
logging.basicConfig(filename='logger.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s : %(levelname)s : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='w'
                    )

reload(sys)
sys.setdefaultencoding('utf8')


class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    file_path = "./"
    logging.info('start init....')
    file_name = "result.xlsx"
    handle_input = HandleInput()
    handle_ip = Handle_ip()
    # 爬取ip到文件
    # handle_ip.crawl_ips()
    # 将ip加载到内存
    handle_ip.load_ip()
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
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=chrome_options)
    # driver = webdriver.Chrome(executable_path="./chromedriver")
    driver.maximize_window()
    input_array = handle_input.ret_array

    def start_requests(self):
        logging.info(u"爬取输入数组:" + json.dumps(self.input_array, ensure_ascii=False, encoding="gb2312"))
        for input_item in self.input_array:
            if self.min_date is None or self.min_date > datetime.strptime(input_item["start_date"], "%Y-%m-%d"):
                self.min_date = datetime.strptime(input_item["start_date"], "%Y-%m-%d")
            if self.max_date is None or self.max_date < datetime.strptime(input_item["end_date"], "%Y-%m-%d"):
                self.max_date = datetime.strptime(input_item["end_date"], "%Y-%m-%d")
            request = scrapy.Request(url=input_item["hotel_url"], callback=self.parse, dont_filter=True)
            input_item["proxy"] = self.handle_ip.random_ip()
            request.meta["item_info"] = input_item
            yield request

    def parse(self, response):
        input_item = response.meta["item_info"]
        # logging.debug(input_item)
        # if input_item["name"] == '上海中航虹桥机场泊悦酒店(中国国际航空公司)' \
        #         or input_item["name"]=='上海新虹桥希尔顿花园酒店' \
        #         or input_item['name']=='希岸酒店(上海虹桥机场国展中心店)':
        with open(input_item["name"] + "_" + input_item["start_date"] + "_" + input_item["end_date"] + ".html",
                  'w') as f:
            f.write(response.body)
        parse = HandleParse(response, datetime.strptime(input_item["start_date"], "%Y-%m-%d"),
                            datetime.strptime(input_item["end_date"], "%Y-%m-%d"), input_item["room_type"],
                            input_item["name"])
        parse.parse(out_map)

    def close(self, reason):
        temp_date = self.min_date
        while temp_date < self.max_date:
            self.file_header.append(temp_date.strftime("%Y-%m-%d"))
            temp_date += timedelta(days=1)
        logging.info(u"解析结果dic:" + json.dumps(out_map, ensure_ascii=False, encoding="gb2312"))
        handle_output = HandleOutput(self.file_path, self.file_name, self.file_header, out_map,
                                     self.input_array)
        handle_output.write()


process = CrawlerProcess(get_project_settings())
process.crawl(DmozSpider)
process.start(stop_after_crawl=False)
