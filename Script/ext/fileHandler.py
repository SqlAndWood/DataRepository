import codecs
import json
import csv

from csv import DictReader
from ext import DataConverter
from ext import FileDetails

class fileHandler:

    # fh = fileHandler(file_name_and_path)
    def __init__(self, file_name_and_path):

        self.file_name_and_path = file_name_and_path

        self.column_headings = self.obtainColumnHeadings()
        self.fd = FileDetails.FileDetails(self.file_name_and_path )
        # Not sure these three are required.
        # self.file_statistics = self.fd.file_statistics
        # self.file_size = self.fd.file_size
        self.file_name = self.fd.file_name

        # print(self.fd.file_directory_path)
        self.data_list_of_dictionaries = self.read_file()

        self.data_nested_list = DataConverter.DataConverter(self.data_list_of_dictionaries).data_nested_list

    def obtainColumnHeadings(self):

        encoding = self.detect_encoding_by_bom('utf-8')

        with open(self.file_name_and_path, "r", encoding=encoding) as file_to_use:
            csv_dict_reader = DictReader(file_to_use)
            return csv_dict_reader.fieldnames

    def read_file(self):

        data_list = []

        # only one in 100 files needs this, but it is enough to cause mischief if it is not implemented.
        encoding = self.detect_encoding_by_bom('utf-8')

        with open(self.file_name_and_path, "r", encoding=encoding) as file_to_use:
            csv_dict_reader = DictReader(file_to_use)

            for row in csv_dict_reader:
                data_list.append(json.loads(json.dumps(row)))

        # might be able to return csv_dict_reader ??
        return (data_list)

    def detect_encoding_by_bom(self, default):

        with open(self.file_name_and_path, 'rb') as f:
            raw = f.read(4)  # will read less if the file is smaller

        # BOM_UTF32_LE's start is equal to BOM_UTF16_LE so need to try the former first
        for enc, boms in \
                ('utf-8-sig', (codecs.BOM_UTF8,)), \
                ('utf-32', (codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE)), \
                ('utf-16', (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):

            if any(raw.startswith(bom) for bom in boms):
                if enc != "":
                    return enc

        return default


    # Probably not a long term solution. Save file to the same folder of original file.
    def SaveTempFile(self, file_name, headings, nested_list):
        file_to_save = self.fd.file_directory_path + file_name
        with open(file_to_save, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            for record in nested_list:
                writer.writerow(record)

