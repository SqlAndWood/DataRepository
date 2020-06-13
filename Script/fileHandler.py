from csv import DictReader

class fileHandler:

    # fh = fileHandler(file_name_and_path)
    def __init__(self, file_name_and_path):
        self.file_name_and_path = file_name_and_path
        self.column_headings = self.obtainColumnHeadings()
        # self.read_file(file_name_and_path)

    def obtainColumnHeadings(self):

        with open(self.file_name_and_path, "r",  encoding='utf-8-sig') as file_to_use:
            csv_dict_reader = DictReader(file_to_use)

            return csv_dict_reader.fieldnames

    # Not used at present
    # def read_file(self):
    #     with open(self.file_name_and_path, "r" , encoding='utf-8-sig') as file_to_use:
    #
    #         for line in file_to_use:
    #             stripped_line = line.strip()
    #             # print(stripped_line)
    #             break
