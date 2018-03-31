import time
from datetime import date

import xlrd


class HanleInput():
    def __init__(self):
        self.now = time.localtime(time.time())
        self.today_str = time.strftime('%Y-%m-%d %H%M%S', self.now)
        self.today_value = time.strftime('%Y-%m-%d', self.now)
        self.output_file_name = str(self.today_str).replace(" ", "_") + ".xls"
        self.input_path = "tasks.xlsx"
        data = xlrd.open_workbook(self.input_path)
        sheets = data.sheets()
        sheet = sheets[0]
        name_array = sheets[0].col_values(0)
        self.ret_array = []
        for i in xrange(1, len(name_array)):
            start_date_value = xlrd.xldate_as_tuple(sheet.col_values(3), data.datemode)
            start_date = date(*start_date_value[:3]).strftime('%Y-%m-%d')
            dep_date_value = xlrd.xldate_as_tuple(sheet.col_values(4), data.datemode)
            dep_date = date(*dep_date_value[:3]).strftime('%Y-%m-%d')
            ret = {"name": sheet.col_values(0),
                   "url": sheet.col_values(1),
                   "room_type": sheet.col_values(2),
                   "start_date": start_date_value,
                   "dep_date": dep_date_value,
                   "default_price": sheet.col_values(5),
                   "day_offset": int(sheet.col_values(6)),
                   }
            self.ret_array.append(ret)
