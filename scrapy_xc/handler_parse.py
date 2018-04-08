# -*- coding: utf-8 -*-
import sys
from datetime import timedelta
import re
import logging

reload(sys)
sys.setdefaultencoding('utf8')
# 通过下面的方式进行简单配置输出方式与日志级别
logging.basicConfig(filename='logger.log', level=logging.INFO)

class HandleParse():
    def __init__(self, response, start_time, end_time, name, room_type):
        self.response = response
        self.start_time = start_time
        self.end_time = end_time
        self.room_type = room_type
        self.name = name


    def parse(self,out_dic):
        if (self.start_time + timedelta(1) == self.end_time):
            return self.day_offset_for_one(out_dic)
        else:
            return self.day_offset_for_more(out_dic)

    def day_offset_for_one(self,out_dic):
        date_roomtype_minPrice_dic = {}
        room_type = ""
        min_room_type = ""
        date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')]={}
        for tr in self.response.xpath("//tr[@brid]"):
            if(len(tr.xpath(".//td[contains(@class,'room_type')]")) > 0):
                room_type = tr.xpath(".//td[contains(@class,'room_type')]")[0].xpath(".//a[contains(@class,'room_unfold')]")[0].root.text.replace("\n","").replace(" ","")
                if(min_room_type == ""):
                    min_room_type = room_type
            if(self.check_tr(tr)):
                price = float(tr.xpath(".//td[contains(@class,'child_name')]")[0].xpath("@data-price")[0].extract())
                if(date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')].has_key(room_type)):
                    minPrice = float(date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][room_type])
                    if(price < minPrice):
                        date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][room_type] = price
                        if(room_type != min_room_type and date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][min_room_type] > price):
                            min_room_type = room_type
                else:
                    date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][room_type] = price
                    if(room_type != min_room_type and date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][min_room_type] > price):
                        min_room_type = room_type
        self.write_to_out_dic(date_roomtype_minPrice_dic,out_dic,min_room_type)

    def day_offset_for_more(self,out_dic):
        date_roomtype_minPrice_dic = {}
        date = self.start_time
        while True:
            date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')] = {}
            date = date + timedelta(1)
            if (date >= self.end_time):
                break


    def check_tr(self, tr):
        if(len(tr.xpath(".//td[contains(@class,'child_name')]")) == 0):
            return False
        if(len(tr.xpath(".//td[contains(@class,'child_name')]")[0].xpath("@data-price")) == 0):
            return False
        if(len(tr.xpath("//span[contains(@class,'supplier_log')]")) > 0 ):
            return False
        confirm_green_elements = tr.xpath("//span[contains(@class,'confirm_green')]")
        if(len(confirm_green_elements) > 0):
            confirm_text = confirm_green_elements[0].root.text.encode("utf-8").replace("\n"," ").replace(" ","")
            if("小时内" in confirm_text):
                hours = self.get_confirm_time(confirm_text)
                if(hours > 1L):
                    return False
        return  True


    def get_confirm_time(self, str):
        return float(re.findall(r"\d+\.?\d*", str)[0])

    def write_to_out_dic(self,date_roomtype_minPrice_dic,out_dic,min_room_type):
        out_dic[self.name] = {}
        for date_str in date_roomtype_minPrice_dic:
            if (date_roomtype_minPrice_dic[date_str].has_key(self.room_type)):
                out_dic[self.name][date_str]={}
                out_dic[self.name][date_str]["price"]=date_roomtype_minPrice_dic[date_str][self.room_type]
                out_dic[self.name][date_str]["type"]=self.room_type
            else:
                out_dic[self.name][date_str] = {}
                if(min_room_type == ""):
                    logging.info(self.name)
                    logging.info(date_str)
                    out_dic[self.name][date_str]["price"] = "-1"
                    out_dic[self.name][date_str]["type"] = self.room_type
                else:
                    out_dic[self.name][date_str]["price"] = date_roomtype_minPrice_dic[date_str][min_room_type]
                    out_dic[self.name][date_str]["type"] = min_room_type