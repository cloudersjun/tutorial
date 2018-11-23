# -*- coding: utf-8 -*-
import json
import logging
import sys
from datetime import datetime, timedelta

import scrapy
from scrapy import settings
import scrapy.spiders
from scrapy import Spider
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
import scrapy.spiders
import scrapy.squeues
import scrapy.statscollectors
import scrapy.utils.conf
import scrapy.utils.deprecate
import scrapy.utils.engine
import scrapy.utils.project
import scrapy.utils.python
import scrapy.utils.template
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scrapy_xc.handle_input import HandleInput
from scrapy_xc.handle_output import HandleOutput
from scrapy_xc.handler_parse import HandleParse
import scrapy_xc.spiders
import scrapy_xc.settings
from scrapy_xc.middlewares import downloadwebkit

# 通过下面的方式进行简单配置输出方式与日志级别
logging.basicConfig(filename='logger.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s : %(levelname)s : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='w'
                    )

reload(sys)
sys.setdefaultencoding('utf8')

handle_input = HandleInput()
input_array = handle_input.ret_array
out_map = {}
file_header = ["name", "room_type"]


class DmozSpider(Spider):
    name = 'dmoz'
    logging.info('start init....')
    # handle_ip = Handle_ip()
    # 爬取ip到文件
    # handle_ip.crawl_ips()
    # 将ip加载到内存
    # handle_ip.load_ip()
    # {"name":，"room_type":,"price_dic":{"date":,"price":}]}
    max_date = None
    min_date = None
    logging.info("init browser....")
    chrome_options = Options()
    # chrome_options.set_headless(True)
    # 不加载图片
    # prefs = {"profile.managed_default_content_settings.images": 2,
    #          "profile.managed_default_content_settings.cookies": 2}
    prefs = {"profile.managed_default_content_settings.cookies": 2}
    # 禁用cookie
    # prefs = {"profile.default_content_settings.cookies": 2, "profile.use-new-accept-language-header": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("lang=zh-CN;en-Us;en;zh;zh-TW")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('disable-infobars')
    # chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--disable-java")
    # chrome_options.add_argument("disable-infobars")
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=chrome_options)
    # driver = webdriver.Chrome(executable_path="./chromedriver")
    # driver.maximize_window()
    # driver.fullscreen_window()
    meta_info = {}

    def start_requests(self):
        logging.info(u"爬取输入数组:" + json.dumps(input_array, ensure_ascii=False, encoding="gb2312"))
        for input_item in input_array:
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
        logging.debug(input_item)
        parse = HandleParse(response, datetime.strptime(input_item["start_date"], "%Y-%m-%d"),
                            datetime.strptime(input_item["end_date"], "%Y-%m-%d"), input_item["room_type"],
                            input_item["name"])
        global out_map
        parse.parse(out_map)
        logging.info(json.dumps(out_map, ensure_ascii=False, encoding="gb2312"))

    def close(self, reason):
        temp_date = self.min_date
        while temp_date < self.max_date:
            file_header.append(temp_date.strftime("%Y-%m-%d"))
            temp_date += timedelta(days=1)
        file_path = "./result/"
        now = datetime.now().strftime("%Y%m%d %H%M%S")
        file_name = now.replace(" ", "_") + ".xlsx"
        logging.info(u"解析结果dic:" + json.dumps(out_map, ensure_ascii=False, encoding="gb2312"))
        logging.info(u"最终写入文件：" + file_name)
        handle_output = HandleOutput(file_path, file_name, file_header, out_map, input_array)
        handle_output.write()
        logging.info(u"close browser:")
        self.driver.close()


process = CrawlerProcess(get_project_settings())
process.crawl(DmozSpider)
process.start()
