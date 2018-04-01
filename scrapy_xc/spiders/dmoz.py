# -*- coding: utf-8 -*-
import scrapy
import sys

from scrapy.conf import settings

from scrapy_xc.handle_input import HandleInput
from scrapy_xc.handle_output import HandleOutput

reload(sys)
sys.setdefaultencoding('utf8')


class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    # allowed_domains = ['dmoz.org']
    # start_urls = ["http://hotels.ctrip.com/hotel/396401.html#ctm_ref=hod_dl_map_ htllst_n_9"]
    print('start init....')

    def start_requests(self):
        handle_input =  HandleInput()
        # handle_input.__init__()
        inpu_array = handle_input.ret_array
        for input_item in inpu_array:
            print(input_item)
            request = scrapy.Request(url=input_item["hotel_url"], callback=self.parse, dont_filter=True)
            request.meta["item_info"] = input_item
            yield request

    def parse(self, response):
        input_item = response.meta["item_info"]
        if settings["DEBUG"]:
            print(input_item)
        # with open("response.html", 'w') as f:
        #     f.write(response.body)
        # print(response.body)
        out_array=[]
        for sel in response.xpath("//tr[@brid]"):
            print(sel)
            out_array.append([sel,"d","1","1"])
        handle_output = HandleOutput("D:\\test\\","test.xls",["name","date","room_type","price"],out_array)
        handle_output.write()
        pass
