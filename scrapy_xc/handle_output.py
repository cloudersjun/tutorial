import os

import xlrd


class HandleOutput():
    def __init__(self):
        self.output_path=""
        self.output_file_name =""

    def write(self,result_array):
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)
        if os.path.exists(self.output_path+self.output_file_name):
            os.remove(self.output_path+self.output_file_name)
            excel = xlrd.open_workbook(filename=self.output_path+self.output_file_name, formatting_info=True)
            #todo 将array写到Excel中