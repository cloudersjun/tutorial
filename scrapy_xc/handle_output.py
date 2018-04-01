# -*- coding: utf-8 -*-
import os

import xlrd
import xlwt
from xlutils.copy import copy
import sys

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
        for col in xrange(0, len(self.header)):
            sheet.write(row, col, self.header[col].decode('utf-8'))
        row = 1
        for result in self.result_array:
            for col in xrange(0, len(result)):
                sheet.write(row, col, result[col].decode('utf-8'))
            row += 1
        book.save(self.output_path + self.output_file_name)