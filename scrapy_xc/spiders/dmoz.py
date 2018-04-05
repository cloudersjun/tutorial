# -*- coding: utf-8 -*-
import sys

import scrapy
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
    file_path = "/Users/yujun/gitPro/tutorial/"
    file_name = "result.xls"
    handle_input = HandleInput()
    out_array = []

    def start_requests(self):
        # handle_input.__init__()
        inpu_array = self.handle_input.ret_array
        for input_item in inpu_array:
            print(input_item)
            request = scrapy.Request(url=input_item["hotel_url"], callback=self.parse, dont_filter=True)
            request.meta["item_info"] = input_item
            yield request

    def parse(self, response):
        input_item = response.meta["item_info"]
        if settings["DEBUG"]:
            print(input_item)
        with open(input_item["name"] + "_" + input_item["start_date"] + "_" + input_item["end_date"] + ".html",
                  'w') as f:
            f.write(response.body)
        for sel in response.xpath("//tr[@brid]"):
            print(sel)
            self.out_array.append([sel.extract(), "d", "1", "1"])
        pass

    def close(self, reason):
        handle_output = HandleOutput(self.file_path, self.file_name, ["name", "date", "room_type", "price"],
                                     self.out_array)
        handle_output.write()
