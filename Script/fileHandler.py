from csv import DictReader
import json

class fileHandler:

    # fh = fileHandler(file_name_and_path)
    def __init__(self, file_name_and_path):

        self.file_name_and_path = file_name_and_path

        self.column_headings = self.obtainColumnHeadings()

        self.obtainFileDetails()

        self.data_list_of_dictionaries = self.read_file()

        self.data_nested_list = self.createNestedList()

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
                # print(row)
                data_list.append(json.loads(json.dumps(row)))


        # might be able to return csv_dict_reader ??
        return(data_list)

    # https://snakify.org/en/lessons/two_dimensional_lists_arrays/

    def createNestedList(self):

        # if isinstance(self.data_list , list):
        #     print('list of..')

        record = []

        for n in self.data_list_of_dictionaries :
            # if isinstance(n, dict):
            #     print('dict of ...')
            # https://www.ict.social/python/basics/multidimensional-lists-in-python
            column = []
            for value in list(n.values()):
                column.append(value)

            record.append(column)

        return record

    def obtainFileDetails(self):
        import os

        self.file_statistics = os.stat(self.file_name_and_path )

        self.file_size = self.file_statistics.st_size
        self.file_name = os.path.basename(self.file_name_and_path)

        pass