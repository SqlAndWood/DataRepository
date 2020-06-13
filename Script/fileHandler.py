from csv import DictReader

import time
import json

class fileHandler:

    # fh = fileHandler(file_name_and_path)
    def __init__(self, file_name_and_path):
        self.file_name_and_path = file_name_and_path
        self.column_headings = self.obtainColumnHeadings()
        self.data_list = self.read_file()

    def obtainColumnHeadings(self):

        with open(self.file_name_and_path, "r",  encoding='utf-8-sig') as file_to_use:
            csv_dict_reader = DictReader(file_to_use)

            return csv_dict_reader.fieldnames


    def read_file(self):

        data_list = []

        with open(self.file_name_and_path, "r", encoding='utf-8-sig') as file_to_use:
            csv_dict_reader = DictReader(file_to_use)

            #this may not be necessary
            for row in csv_dict_reader:
                data_list.append(json.loads(json.dumps(row)))


        # might be able to return csv_dict_reader ??
        return(data_list)

