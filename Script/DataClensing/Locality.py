import os
import time

import pandas as pd

from fileHandler import *


class Locality:
    # unsure how, but the globals should probably be stored in a seperate JSON file?
    global folder_location
    folder_location = "..\Data\\"

    global file_name
    file_name = 'australian_postcodes.json'

    global locality_columns_to_append
    locality_columns_to_append = ['locality', 'state', 'postcode']

    # l = DataClensing(file_name_and_path)
    def __init__(self, window, DATA_GRID_COL_HEADINGS, DATA_GRID_NESTED_LIST, column_to_resolve):

        start_time = time.time()

        # TODO: ONLY RUN THIS CODE IF IT HAS NOT ALREADY BEEN EXECUTED FOR 'THIS' column_to_resolve PRIOR.

        self.display_ever_x_rows = 40

        self.column_to_resolve = column_to_resolve
        self.window = window
        self.column_headings = DATA_GRID_COL_HEADINGS
        self.temp_data_nested_list = DATA_GRID_NESTED_LIST
        self.column_pos_to_resolve = self.obtainColumnPositions()
        self.appendColumnHeadings()
        self.data_nested_list = self.process()
        self.time_to_execute_seconds = (time.time() - start_time)

    def updateStatusBar(self, message, override_previous):

        self.window.FindElement('_STATUSBAR_').Update(message, append=False)
        self.window.Refresh()

    def obtainColumnPositions(self):
        pos = 0
        for col in self.column_headings:
            if col == self.column_to_resolve:
                print('l', col, 'p', pos)
                return pos

            pos += 1

    def appendColumnHeadings(self):
        # TODO: Test TO SEE IF THE COLUMN ALREADY EXISTS
        for column in locality_columns_to_append:
            self.column_headings.append(self.column_to_resolve + "_" + column)

    def process(self):
        record = []

        cur_loop_pos = 0

        for row in self.temp_data_nested_list:

            start_time = time.time()
            la = self.resolveAddress(row[self.column_pos_to_resolve])

            for column in locality_columns_to_append:

                if la is not None:
                    row.append(la.get(column))
                else:
                    row.append('')

            if cur_loop_pos % self.display_ever_x_rows != 0:
                self.updateStatusBar(row, True)

            cur_loop_pos += 1
            row.append(time.time() - start_time)

            record.append(row)

        return (record)

    def resolveAddress(self, provided_address):

        start_time = time.time()

        australian_location_data = self.loadAustralianLocationData()

        dict_of_matched_locations = self.createDictionaryOfMatchedLocationData(australian_location_data,
                                                                               provided_address)

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

    def readJSON(self, file_name_and_path):
        with open(file_name_and_path) as json_file:
            return json.load(json_file)

    # this does not prefernce a SA key over any other state/territory
    def createDictionaryOfMatchedLocationData(self, dict_location, provided_address):

        dic_identified = []

        for individual_key in dict_location:

            score = 0.0

            individual_key['location_len'] = self.observeLocation(provided_address, individual_key)

            # temporary while I figure out how I'd like the algorithm to be.
            if individual_key.get('locality').upper() in provided_address.upper() and individual_key.get(
                    'postcode') in provided_address.upper() and individual_key.get('state') == 'SA':
                score += 1.0

            if individual_key.get('locality').upper() in provided_address.upper() and individual_key.get(
                    'postcode') == 'SA':
                score += 1.0

            if individual_key.get(
                    'locality').upper() in provided_address.upper():  # and individual_key.get('postcode') in provided_address.upper():
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
    def obtainSingleMostLikelyAddress(self, dict_ofMatchedLocations):

        dic_sortedOnScore = sorted(dict_ofMatchedLocations, key=lambda i: (i['score'], i['location_len']), reverse=True)

        for sk in dic_sortedOnScore:
            # return the first found Address.
            return sk
            break

    def observeLocation(self, provided_address, individual_key):

        if individual_key.get('locality').upper() in provided_address.upper():
            return len(individual_key.get('locality').upper())
        else:
            return -1
