# -*- coding: utf-8 -*-
import scrapy
import sys

from scrapy_xc.handle_input import HandleInput

reload(sys)
sys.setdefaultencoding('utf8')


class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    # allowed_domains = ['dmoz.org']
    start_urls = ["http://hotels.ctrip.com/hotel/396401.html#ctm_ref=hod_dl_map_ htllst_n_9"]
    print('start init....')

    def start_requests(self):
        handle_input =  HandleInput()
        # handle_input.__init__()
        inpu_array = handle_input.ret_array
        for input_item in inpu_array:
            print(input_item)
            request = scrapy.Request(url=input_item["hotel_url"], callback=self.parse, dont_filter=True)
            request.meta["start_date"] = input_item["start_date"]
            request.meta["end_date"] = input_item["end_date"]

    def parse(self, response):
        with open("response.html", 'w') as f:
            f.write(response.body)
        # print(response.body)
        pass
