# coding=utf-8
import json
from random import choice

import requests
from scrapy import Selector


class Handle_ip:
    def __init__(self):
        self.ip_list = []
        self.file_name = "ip.ini"

    def crawl_ips(self):
        """
        爬取西刺网的免费代理IP
        """
        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4"
        }
        for i in range(2):
            re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
            selector = Selector(text=re.text)
            all_trs = selector.css("#ip_list tr")
            ip_list = []
            for tr in all_trs[1:]:
                speed_str = tr.css(".bar::attr(title)").extract()[0]
                ip = tr.css("td:nth-child(2)::text").extract_first()
                port = tr.css("td:nth-child(3)::text").extract_first()
                proxy_type = tr.css("td:nth-child(6)::text").extract_first()
                if speed_str:
                    speed = float(speed_str.split("秒")[0])
                    if speed > 3:
                        continue
                ip_list.append((ip, port, proxy_type, speed))
            with open(self.file_name, 'w') as f:
                for ip_info in ip_list:
                    f.writelines(str(ip_info[2]).lower()+"://"+str(ip_info[0])+":"+str(ip_info[1]) + "\n")
                f.close()

    def load_ip(self):
        with open(self.file_name, "r") as f:
            self.ip_list = f.readlines()
        f.close()

    def random_ip(self):
        return choice(self.ip_list).replace("\n", "")
