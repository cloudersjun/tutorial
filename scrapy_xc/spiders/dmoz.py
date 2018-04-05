# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timedelta

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
    file_path = "./"
    file_name = "result.xls"
    handle_input = HandleInput()
    # {"name":，"room_type":,"price_dic":{"date":,"price":}]}
    out_array = []
    file_header = ["name", "room_type"]
    max_date = None
    min_date = None

    def start_requests(self):
        # handle_input.__init__()
        input_array = self.handle_input.ret_array
        print  len(input_array)
        print input_array
        for input_item in input_array:
            print(input_item)
            if self.min_date is None or self.min_date > datetime.strptime(input_item["start_date"], "%Y-%m-%d"):
                self.min_date = datetime.strptime(input_item["start_date"], "%Y-%m-%d")
            if self.max_date is None or self.max_date < datetime.strptime(input_item["end_date"], "%Y-%m-%d"):
                self.max_date = datetime.strptime(input_item["end_date"], "%Y-%m-%d")
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
            ret_item = {}
            ret_item['name'] = sel.extract()
            ret_item['room_type'] = "rrr"
            ret_item["price_dic"] = {}
            ret_item["price_dic"]["date"] = "2018-04-03"
            ret_item["price_dic"]["price"] = 2
            self.out_array.append(ret_item)
        pass

    def close(self, reason):
        temp_date = self.min_date
        while temp_date <= self.max_date:
            self.file_header.append(temp_date.strftime("%Y-%m-%d"))
            temp_date += timedelta(days=1)
        handle_output = HandleOutput(self.file_path, self.file_name, self.file_header, self.out_array)
        #handle_output.write()

