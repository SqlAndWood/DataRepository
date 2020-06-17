import os, time

class FileDetails:

    # fh = fileDetails(file_name_and_path)
    def __init__(self, file_name_and_path):

        self.file_name_and_path = file_name_and_path

        self.file_directory_path = os.path.dirname(os.path.realpath(file_name_and_path)) + "\\"

        self.file_statistics = os.stat(self.file_name_and_path)

        self.file_size = self.file_statistics.st_size
        self.file_name = os.path.basename(self.file_name_and_path)

        self.file_created_date =time.ctime(os.path.getctime(self.file_name_and_path))

        self.file_modified_date =time.ctime(os.path.getmtime(self.file_name_and_path))