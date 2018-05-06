# -*- coding: utf-8 -*-
import json
import logging
import sys
from datetime import datetime, timedelta

import scrapy
import scrapy.core.downloader
import scrapy.core.downloader.contextfactory
import scrapy.core.downloader.handlers.http
import scrapy.core.downloader.middleware
import scrapy.core.engine
import scrapy.core.scheduler
import scrapy.core.scraper
import scrapy.core.spidermw
import scrapy.downloadermiddlewares.ajaxcrawl
import scrapy.downloadermiddlewares.cookies
import scrapy.downloadermiddlewares.decompression
import scrapy.downloadermiddlewares.defaultheaders
import scrapy.downloadermiddlewares.downloadtimeout
import scrapy.downloadermiddlewares.httpauth
import scrapy.downloadermiddlewares.httpcache
import scrapy.downloadermiddlewares.httpcompression
import scrapy.downloadermiddlewares.httpproxy
import scrapy.downloadermiddlewares.redirect
import scrapy.downloadermiddlewares.retry
import scrapy.downloadermiddlewares.robotstxt
import scrapy.downloadermiddlewares.stats
import scrapy.downloadermiddlewares.useragent
import scrapy.dupefilters
import scrapy.exceptions
import scrapy.extensions.closespider
import scrapy.extensions.corestats
import scrapy.extensions.debug
import scrapy.extensions.feedexport
import scrapy.extensions.httpcache
import scrapy.extensions.logstats
import scrapy.extensions.memdebug
import scrapy.extensions.memusage
import scrapy.extensions.spiderstate
import scrapy.extensions.statsmailer
import scrapy.extensions.telnet
import scrapy.extensions.throttle
import scrapy.logformatter
import scrapy.pipelines
import scrapy.spiderloader
import scrapy.spidermiddlewares.depth
import scrapy.spidermiddlewares.httperror
import scrapy.spidermiddlewares.offsite
import scrapy.spidermiddlewares.referer
import scrapy.spidermiddlewares.urllength
import scrapy.squeues
import scrapy.statscollectors
import scrapy.utils.conf
import scrapy.utils.deprecate
import scrapy.utils.engine
import scrapy.utils.project
import scrapy.utils.python
import scrapy.utils.template
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scrapy_xc.handle_input import HandleInput
from scrapy_xc.handle_output import HandleOutput
from scrapy_xc.handler_parse import HandleParse

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
    # handle_ip = Handle_ip()
    # 爬取ip到文件
    # handle_ip.crawl_ips()
    # 将ip加载到内存
    # handle_ip.load_ip()
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
    prefs = {"profile.managed_default_content_settings.images": 2, "profile.managed_default_content_settings.cookies": 2}
    # 禁用cookie
    # prefs = {"profile.default_content_settings.cookies": 2, "profile.use-new-accept-language-header": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("Accept-Language= en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6")
    chrome_options.add_argument("-use-new-accept-language-header")
    # chrome_options.add_argument("--disable-local-storage")
    # chrome_options.add_argument("--use-new-accept-language-header")
    # chrome_options.add_argument("--disable-session-storage")、
    chrome_options.add_argument("--start-maximized")
    desired_capabilities = chrome_options.to_capabilities()
    # chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--disable-java")
    # chrome_options.add_argument("disable-infobars")
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=chrome_options)
    # driver = webdriver.Chrome(executable_path="./chromedriver.exe")
    # driver.maximize_window()
    # driver.fullscreen_window()
    # 携带cookie打开
    # driver.add_cookie({'name': 'ABC', 'value': 'DEF'})
    input_array = handle_input.ret_array
    meta_info = {}

    def start_requests(self):
        logging.info(u"爬取输入数组:" + json.dumps(self.input_array, ensure_ascii=False, encoding="gb2312"))
        for input_item in self.input_array:
            if self.min_date is None or self.min_date > datetime.strptime(input_item["start_date"], "%Y-%m-%d"):
                self.min_date = datetime.strptime(input_item["start_date"], "%Y-%m-%d")
            if self.max_date is None or self.max_date < datetime.strptime(input_item["end_date"], "%Y-%m-%d"):
                self.max_date = datetime.strptime(input_item["end_date"], "%Y-%m-%d")
            request = scrapy.Request(url=input_item["hotel_url"], callback=self.parse, dont_filter=True)
            # input_item["proxy"] = self.handle_ip.random_ip()
            request.meta["item_info"] = input_item
            yield request

    def parse(self, response):
        input_item = response.meta["item_info"]
        # logging.debug(input_item)
        # if input_item["name"] == '上海中航虹桥机场泊悦酒店(中国国际航空公司)' \
        #         or input_item["name"]=='上海新虹桥希尔顿花园酒店' \
        #         or input_item['name']=='希岸酒店(上海虹桥机场国展中心店)':
        # with open(input_item["name"] + "_" + input_item["start_date"] + "_" + input_item["end_date"] + ".html",
        #           'w') as f:
        #     f.write(response.body)
        parse = HandleParse(response, datetime.strptime(input_item["start_date"], "%Y-%m-%d"),
                            datetime.strptime(input_item["end_date"], "%Y-%m-%d"), input_item["room_type"],
                            input_item["name"])
        parse.parse(out_map)

    def close(self, reason):
        logging.info(u"close brower")
        self.driver.close()
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
process.start(stop_after_crawl=True)
