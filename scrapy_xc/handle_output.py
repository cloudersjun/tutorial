# -*- coding: utf-8 -*-
import os
import sys

import xlwt

reload(sys)
sys.setdefaultencoding('utf8')


class HandleOutput():
    def __init__(self, path, name, header, result_array):
        self.output_path = path
        self.output_file_name = name
        self.header = header
        self.result_array = result_array

    def write(self):
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)
        if os.path.exists(self.output_path + self.output_file_name):
            os.remove(self.output_path + self.output_file_name)
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        sheet = book.add_sheet('爬取结果', cell_overwrite_ok=True)
        row, col = 0, 0
        date_map = {}
        for col in xrange(0, len(self.header)):
            sheet.write(row, col, self.header[col].decode('utf-8'))
            date_map[self.header[col]] = col
        row = 1
        for result in self.result_array:
            sheet.write(row, 0, result["name"])
            sheet.write(row, 1, result["room_type"])
            price_map = result["price_dic"]
            for i in xrange(2, len(self.header)):
                price_date = self.header[i]
                if price_map.get(price_date) is not None:
                    price = price_map.get(price_date)
                    if price == -1:
                        self.color_cell(sheet, row, i, 2500)
                    else:
                        sheet.write(row, i, price)
            row += 1
        book.save(self.output_path + self.output_file_name)

    def color_cell(self, sheet, row, col, content):
        xlwt_temp = xlwt
        style = xlwt_temp.XFStyle()  # 初始化样式
        pattern = xlwt_temp.Pattern()  # 为样式创建图案
        pattern.pattern = 1  # 设置底纹的图案索引，1为实心，2为50%灰色，对应为excel文件单元格格式中填充中的图案样式
        pattern.pattern_fore_colour = 10  # 设置底纹的前景色，对应为excel文件单元格格式,红色中填充中的背景色
        pattern.pattern_back_colour = 35  # 设置底纹的背景色，对应为excel文件单元格格式中填充中的图案颜色
        style.pattern = pattern  # 为样式设置图案
        sheet.write(row, col, unicode(content), style)
