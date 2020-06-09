import json  # read the JSON file containing authentication details.
import pandas as pd

def main():
    # folder_path = os.path.abspath(os.path.dirname("..\mapping\\"))
    # file_name = 'keywords.json'
    # return ReadJSON(folder_path, file_name)
    pass


def readJSON(folder_path, file_name):
    return readJSONfromPath(folder_path + "\\" + file_name)


def readJSONfromPath(file_name_and_path):
    with open(file_name_and_path) as json_file:
        return json.load(json_file)



def readJSONtoDataFrame(folder_path, file_name):
    return readJSONtoDataFramefromPath(folder_path + "\\" + file_name)


def readJSONtoDataFramefromPath(file_name_and_path):
    with open(file_name_and_path) as json_file:
        return pd.read_json(json_file)



if __name__ == "__main__":
    main()