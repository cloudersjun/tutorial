# -*- coding: utf-8 -*-
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    # allowed_domains = ['dmoz.org']
    start_urls =  ["http://hotels.ctrip.com/hotel/396401.html#ctm_ref=hod_dl_map_ htllst_n_9"]
    print('start init....')
    def parse(self, response):
        with open("response.html",'w') as f:
            f.write(response.body)
        # print(response.body)
        pass
