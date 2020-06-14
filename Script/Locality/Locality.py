import pandas as pd
import os
import time


from DataConverter import *
from fileHandler import *

class Locality:

    global locality_columns_to_append
    locality_columns_to_append = ['locality','state','postcode']

    global folder_location
    folder_location = "..\Data\\"

    global file_name
    file_name = 'australian_postcodes.json'

    # l = Locality(file_name_and_path)
    def __init__(self, window, file_name_and_path, column_to_resolve):

        start_time = time.time()

        self.file_name_and_path = file_name_and_path
        self.column_to_resolve = column_to_resolve
        self.window = window

        fh = fileHandler(file_name_and_path)

        self.column_headings = fh.column_headings
        self.appendColumnHeadings()

        # Ultimatly we want to create an 'array' containing the data to return to present on thh main form.
        self.data_list = []
        self.data_list = self.read_file()

        # This is really important, although, it is a long winded operation to do so.

        self.data_nested_list = DataConverter(self.data_list).data_nested_list

        self.time_to_execute_seconds = (time.time() - start_time)

    def updateStatusBar(self,  message, override_previous):
        # if override_previous == True:
        self.window.FindElement('_STATUSBAR_').Update('')
        self.window.Refresh()
        self.window.FindElement('_STATUSBAR_').Update(message, append=False)
        self.window.Refresh()


    def appendColumnHeadings(self):

        for column in locality_columns_to_append:
            self.column_headings.append(self.column_to_resolve + "_" + column)


    def read_file(self):

        data_list = []

        with open(self.file_name_and_path, "r", encoding='utf-8-sig') as file_to_use:
            csv_dict_reader = DictReader(file_to_use)

            for row in csv_dict_reader:
                start_time = time.time()
                la = self.resolveAddress(row[self.column_to_resolve])

                for column in locality_columns_to_append:
                    # self.column_headings.append(column)

                    if la is not None:
                        row[self.column_to_resolve + "_" + column] = la[column]
                    else:
                        row[self.column_to_resolve + "_" + column] = ''


                # if la is not None:
                #     print(row[self.column_to_resolve] , ' : ', row)
                self.updateStatusBar(la, True)

                row['seconds'] = (time.time() - start_time)
                data_list.append(json.loads(json.dumps(row)))

        return(data_list)


    def resolveAddress(self,provided_address):

        start_time = time.time()

        australian_location_data = self.loadAustralianLocationData()

        dict_of_matched_locations = self.createDictionaryOfMatchedLocationData(australian_location_data, provided_address)

        likely_address = self.obtainSingleMostLikelyAddress(dict_of_matched_locations)

        if likely_address is not None:
            likely_address['seconds'] = (time.time() - start_time)

            return likely_address

        else:
            return None


    def loadAustralianLocationData(self):

        pd.set_option("display.max_rows", 30, "display.max_columns", None)

        mapping_folder_path = os.path.abspath(os.path.dirname(folder_location))
        dict_location = self.readJSON(mapping_folder_path + "\\" + file_name)

        return dict_location

    def readJSON(self,file_name_and_path):
        with open(file_name_and_path) as json_file:
            return json.load(json_file)


    # this does not prefernce a SA key over any other state/territory
    def createDictionaryOfMatchedLocationData(self,dict_location, provided_address):

        dic_identified = []

        for individual_key in dict_location:

            score = 0.0

            individual_key['location_len'] = self.observeLocation(provided_address, individual_key)

            # temporary while I figure out how I'd like the algorithm to be.
            if individual_key.get('locality').upper() in provided_address.upper() and individual_key.get('postcode') in provided_address.upper() and individual_key.get('state') == 'SA':
                score += 1.0

            if individual_key.get('locality').upper() in provided_address.upper() and individual_key.get('postcode') == 'SA':
                score += 1.0

            if individual_key.get('locality').upper() in provided_address.upper() : #and individual_key.get('postcode') in provided_address.upper():
                score += 1.0

            if individual_key.get('postcode').upper() in provided_address.upper():
                score += 0.5

            if provided_address.upper() in 'SA':
                score += 0.5

            if score > 1:

                individual_key['score'] = score

                dic_identified.append(individual_key)

        return dic_identified


    # This is a fuzzy adress match. Only one address is to be matched, as the most likely match.
    # matching the incorrect address is not a key issue here.
    def obtainSingleMostLikelyAddress(self,dict_ofMatchedLocations):

        dic_sortedOnScore = sorted(dict_ofMatchedLocations, key=lambda i: (i['score'], i['location_len']), reverse=True)

        for sk in dic_sortedOnScore:
            return sk
            break


    def observeLocation(self,provided_address, individual_key):

        if individual_key.get('locality').upper() in provided_address.upper():
            return len(individual_key.get('locality').upper())
        else:
            return -1