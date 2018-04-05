import time
from datetime import timedelta, datetime

import xlrd
from xlrd import xldate_as_tuple


class HandleInput:
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
            start_date = datetime(*xldate_as_tuple(sheet.col_values(3)[i], 0))
            dep_date = datetime(*xldate_as_tuple(sheet.col_values(4)[i], 0))
            day_offset = int(sheet.col_values(6)[i])
            offset_days = timedelta(days=day_offset)
            temp_date = start_date
            while temp_date + offset_days <= dep_date:
                ret = {"name": sheet.col_values(0)[i], "hotel_url": sheet.col_values(1)[i],
                       "room_type": sheet.col_values(2)[i], "default_price": sheet.col_values(5)[i],
                       "start_date": temp_date.strftime('%Y-%m-%d'),
                       "end_date": (temp_date + offset_days).strftime('%Y-%m-%d')}
                self.ret_array.append(ret)
                temp_date = temp_date + offset_days
            if temp_date != dep_date:
                ret = {"name": sheet.col_values(0)[i], "hotel_url": sheet.col_values(1)[i],
                       "room_type": sheet.col_values(2)[i],
                       "default_price": sheet.col_values(5)[i],
                       "start_date": temp_date.strftime('%Y-%m-%d'),
                       "end_date": dep_date.strftime('%Y-%m-%d')}
                self.ret_array.append(ret)
