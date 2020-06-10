from csv import DictReader

def ObtainFileHeader(file_name_and_path):

    with open(file_name_and_path, 'r') as file_to_use:

        csv_dict_reader = DictReader(file_to_use)

        column_names = csv_dict_reader.fieldnames

        return column_names