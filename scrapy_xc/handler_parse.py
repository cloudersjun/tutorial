# -*- coding: utf-8 -*-
import sys
from datetime import timedelta
import re
import json
reload(sys)
sys.setdefaultencoding('utf8')


class HandleParse():
    def __init__(self, response, start_time, end_time, room_type, name):
        self.response = response
        self.start_time = start_time
        self.end_time = end_time
        self.room_type = room_type
        self.name = name
        # self.price_annotation = "@data-pricedisplay"
        self.price_annotation = "@data-price"


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
        if(len(self.response.xpath("//tr[@brid]")) == 0):
            if (len(self.response.xpath(".//div[contains(@class,'room_list_loading')]")) == 0):
                date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][self.room_type] = {}
                date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][self.room_type]["price"] = "-1"
                date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][self.room_type]["hour"] = 0
                min_room_type = self.room_type
            else:
                date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][self.room_type] = {}
                date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][self.room_type]["price"]=0
                date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][self.room_type]["hour"] = 0
                min_room_type = self.room_type
        else:
            isNotHasWindow = False
            for tr in self.response.xpath("//tr[@brid]"):
                if(len(tr.xpath(".//td[contains(@class,'room_type')]")) > 0):
                    isNotHasWindow = False
                    room_type = tr.xpath(".//td[contains(@class,'room_type')]")[0].xpath(".//a[contains(@class,'room_unfold')]")[0].root.text.replace("\n","").replace(" ","")
                    if ("无窗" in room_type):
                        isNotHasWindow = True
                        continue
                    if(min_room_type==""):
                        min_room_type = room_type
                if(self.check_tr(tr) and not isNotHasWindow):
                    # price = float(tr.xpath(".//td[contains(@class,'child_name')]")[0].xpath("@data-price")[0].extract())
                    price = float(tr.xpath(".//td[contains(@class,'child_name')]")[0].xpath(self.price_annotation)[0].extract())
                    if(price == 0):
                        continue
                    if(date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')].has_key(room_type)):
                        minPrice = float(date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][room_type]["price"])
                        if(price < minPrice):
                            date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][room_type]["price"] = price
                            if(self.check_hour(tr)):
                                date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][room_type]["hour"] = 1
                            else:
                                date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][room_type]["hour"] = 0
                            if(room_type != min_room_type and date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][min_room_type]["price"] > price):
                                min_room_type = room_type
                    else:
                        date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][room_type] = {}
                        date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][room_type]["price"] = price
                        if (self.check_hour(tr)):
                            date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][room_type]["hour"] = 1
                        else:
                            date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][room_type]["hour"] = 0
                        if(date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')].has_key(min_room_type)):
                            if(room_type != min_room_type and date_roomtype_minPrice_dic[self.start_time.strftime('%Y-%m-%d')][min_room_type]["price"] > price):
                                min_room_type = room_type
                        else:
                            min_room_type = room_type
        min_room_type_dic = {}
        min_room_type_dic[self.start_time.strftime('%Y-%m-%d')] = min_room_type
        self.write_to_out_dic(date_roomtype_minPrice_dic,out_dic,min_room_type_dic)

    def day_offset_for_more(self,out_dic):
        date_roomtype_minPrice_dic = {}
        min_room_type_dic = {}
        date = self.start_time
        num = 0
        while True:
            date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')] = {}
            room_type = ""
            min_room_type = ""
            if (len(self.response.xpath("//tr[@brid]")) == 0):
                if (len(self.response.xpath(".//div[contains(@class,'room_list_loading')]")) == 0):
                    date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')][self.room_type] = {}
                    date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')][self.room_type]["price"] = "-1"
                    date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')][self.room_type]["hour"] = 0
                    min_room_type = self.room_type
                else:
                    date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')][self.room_type] = {}
                    date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')][self.room_type]["price"] = 0
                    date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')][self.room_type]["hour"] = 0
                    min_room_type = self.room_type
            else:
                isNotHasWindow = False
                for tr in self.response.xpath("//tr[@brid]"):
                    if (len(tr.xpath(".//td[contains(@class,'room_type')]")) > 0):
                        isNotHasWindow = False
                        room_type = \
                        tr.xpath(".//td[contains(@class,'room_type')]")[0].xpath(".//a[contains(@class,'room_unfold')]")[
                            0].root.text.replace("\n", "").replace(" ", "")
                        if("无窗" in room_type):
                            isNotHasWindow = True
                            continue
                        if (min_room_type == ""):
                            min_room_type = room_type
                    if (self.check_tr(tr) and not isNotHasWindow):
                        price_more = json.loads(re.sub(r"{(\w+?):", r"{'\1' :",re.sub(r",(\w+?):", r",'\1' :",re.sub(r"\$\('#(\w+?)'\).value\(\)", r"'test'",str(tr.xpath(".//span[contains(@class,'base_txtdiv')]")[0].xpath("@data-params")[0].extract())))).replace("'","\""))
                        price_str = price_more["options"]["content"]["info"]["1"]["1"][num]["price"]
                        price = -1
                        if(price_str != "满房"):
                            price = float(price_str)
                        if (price>0 and date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')].has_key(room_type)):
                            minPrice = float(date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')][room_type]["price"])
                            if (price < minPrice):
                                date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')][room_type]["price"] = price
                                if(self.check_hour(tr)):
                                    date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')][room_type]["hour"] = 1
                                else:
                                    date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')][room_type]["hour"] = 0
                                if (room_type != min_room_type and
                                            date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')][
                                                min_room_type]["price"] > price):
                                    min_room_type = room_type
                        else:
                            if(price > 0):
                                date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')][room_type] = {}
                                date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')][room_type]["price"] = price
                                if (self.check_hour(tr)):
                                    date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')][room_type]["hour"] = 1
                                else:
                                    date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')][room_type]["hour"] = 0
                                if(date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')].has_key(min_room_type)):
                                    if (room_type != min_room_type and date_roomtype_minPrice_dic[date.strftime('%Y-%m-%d')][min_room_type]["price"] > price):
                                        min_room_type = room_type
                                else:
                                    min_room_type = room_type
            min_room_type_dic[date.strftime('%Y-%m-%d')] = min_room_type
            date = date + timedelta(1)
            num = num +1
            if (date >= self.end_time):
                break
        self.write_to_out_dic(date_roomtype_minPrice_dic, out_dic, min_room_type_dic)

    def check_tr(self, tr):
        if(len(tr.xpath(".//td[contains(@class,'child_name')]"))==0):
            return False
        if(len(tr.xpath(".//td[contains(@class,'child_name')]")[0].xpath(self.price_annotation))==0):
            return False
        if(len(tr.xpath(".//td[contains(@class,'child_name')]")[0].xpath("@data-hourroom")) > 0):
            return False
        if(len(tr.xpath(".//span[contains(@class,'supplier_log')]")) > 0 ):
            return False
        if(len(tr.xpath(".//div[contains(@class,'btns_base22_main')]")) == 0):
            return False
        if(tr.xpath(".//div[contains(@class,'btns_base22_main')]")[0].root.text.replace(" ","") == "订完"):
            return False
        # label_onsale_blue_elements = tr.xpath(".//span[contains(@class,'label_onsale_blue')]")
        # if len(label_onsale_blue_elements) > 0 :
        #     for label_onsale_blue_element in label_onsale_blue_elements :
        #         onsale_text = label_onsale_blue_element.root.text.replace("\n"," ").replace(" ","")
        #         if "代理" in onsale_text :
        #             return False
        confirm_green_elements = tr.xpath(".//span[contains(@class,'confirm_green')]")
        if(len(confirm_green_elements) > 0):
            confirm_text = confirm_green_elements[0].root.text.replace("\n"," ").replace(" ","")
            if("小时内" in confirm_text):
                hours = self.get_confirm_time(confirm_text)
                if(hours > 1):
                    return False
        room_type_elements = tr.xpath(".//a[contains(@class,'room_unfold')]")
        if(len(room_type_elements) > 0):
            room_type_text = room_type_elements[0].root.text.replace("\n"," ").replace(" ","")
            if("无窗" in room_type_text):
                return False
        return  True

    def check_hour(self,tr):
        confirm_green_elements = tr.xpath(".//span[contains(@class,'confirm_green')]")
        if (len(confirm_green_elements) > 0):
            confirm_text = confirm_green_elements[0].root.text.replace("\n", " ").replace(" ", "")
            if ("小时内" in confirm_text):
                hours = self.get_confirm_time(confirm_text)
                if (hours == 1):
                    return True
        return False

    def get_confirm_time(self, str):
        return float(re.findall(r"\d+\.?\d*", str)[0])

    def write_to_out_dic(self,date_roomtype_minPrice_dic,out_dic,min_room_type_dic):
        if(not out_dic.has_key(self.name)):
            out_dic[self.name]={}
        for date_str in date_roomtype_minPrice_dic:
            if(not out_dic[self.name].has_key(date_str)):
                out_dic[self.name][date_str]={}
            if (date_roomtype_minPrice_dic[date_str].has_key(self.room_type)):
                out_dic[self.name][date_str]["price"]=date_roomtype_minPrice_dic[date_str][self.room_type]["price"]
                out_dic[self.name][date_str]["hour"] = date_roomtype_minPrice_dic[date_str][self.room_type]["hour"]
                out_dic[self.name][date_str]["type"]=self.room_type
            else:
                if(date_roomtype_minPrice_dic[date_str].has_key(min_room_type_dic[date_str])):
                    out_dic[self.name][date_str]["price"] = date_roomtype_minPrice_dic[date_str][min_room_type_dic[date_str]]["price"]
                    out_dic[self.name][date_str]["hour"] = date_roomtype_minPrice_dic[date_str][min_room_type_dic[date_str]]["hour"]
                    out_dic[self.name][date_str]["type"] = min_room_type_dic[date_str]
                else:
                    out_dic[self.name][date_str]["price"] = "-1"
                    out_dic[self.name][date_str]["hour"] = 0
                    out_dic[self.name][date_str]["type"] = self.room_type