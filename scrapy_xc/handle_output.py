# -*- coding: utf-8 -*-
import os
import sys

import xlsxwriter

reload(sys)
sys.setdefaultencoding('utf8')


class HandleOutput:
    def __init__(self, path, name, header, result_map, input_array):
        self.output_path = path
        self.output_file_name = name
        self.header = header
        self.result_map = result_map
        self.input_array = input_array

    def write(self):
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)
        if os.path.exists(self.output_path + self.output_file_name):
            os.remove(self.output_path + self.output_file_name)
        book = xlsxwriter.Workbook(self.output_path + self.output_file_name)
        red_format = book.add_format()
        red_format.set_bg_color('red')
        sheet = book.add_worksheet('爬取结果')
        row, col = 0, 0
        date_map = {}
        for col in xrange(0, len(self.header)):
            sheet.write(row, col, self.header[col].decode('utf-8'))
            date_map[self.header[col]] = col
        row = 1
        already_set = set()
        for room_input_info in self.input_array:
            room_name = room_input_info['name']
            if already_set.__contains__(room_name):
                continue
            else:
                sheet.write(row, 0, room_name)
                sheet.write(row, 1, room_input_info["room_type"])
                price_info_map = self.result_map.get(room_name)
                if price_info_map is None:
                    for i in xrange(2, len(self.header)):
                        sheet.write(row, i, 2500, red_format)
                else:
                    for i in xrange(2, len(self.header)):
                        need_comment = False
                        comment = ""
                        price_date = self.header[i]
                        if price_info_map.get(price_date) is None:
                            pass
                        else:
                            price_info = price_info_map.get(price_date)
                            if price_info["hour"] is not None and price_info["hour"] == 1:
                                need_comment = True
                                comment += u"一小时确认"
                            price = price_info["price"]
                            if int(price) == -1:
                                sheet.write(row, i, 2500, red_format)
                                pass
                            else:
                                room_type = price_info["type"]
                                if room_type == room_input_info["room_type"]:
                                    sheet.write(row, i, price)
                                else:
                                    sheet.write(row, i, price)
                                    need_comment = True
                                    comment += room_type
                            if need_comment:
                                sheet.write_comment(row, i, comment)
            already_set.add(room_name)
            row += 1
        book.close()
