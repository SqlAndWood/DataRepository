import pandas as pd
import os
import time
import json

def main():
    provided_address = "as"

    print(resolveAddress(provided_address))
    pass


def resolveAddress(provided_address):

    start_time = time.time()

    australian_location_data = loadAustralianLocationData()

    dict_of_matched_locations = createDictionaryOfMatchedLocationData(australian_location_data, provided_address)

    likely_address = obtainSingleMostLikelyAddress(dict_of_matched_locations)

    if likely_address is not None:
        likely_address['seconds'] = (time.time() - start_time)

        return likely_address

    else:
        return None

def loadAustralianLocationData():

    pd.set_option("display.max_rows", 30, "display.max_columns", None)

    folder_location = "..\Data\\"

    file_name = 'australian_postcodes.json'

    mapping_folder_path = os.path.abspath(os.path.dirname(folder_location))
    dict_location = readJSON(mapping_folder_path + "\\" + file_name)

    return dict_location


def readJSON(file_name_and_path):
    with open(file_name_and_path) as json_file:
        return json.load(json_file)

# this does not prefernce a SA key over any other state/territory
def createDictionaryOfMatchedLocationData(dict_location, provided_address):

    dic_identified = []

    for individual_key in dict_location:

        score = 0.0

        individual_key['location_len'] = observeLocation(provided_address, individual_key)

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
def obtainSingleMostLikelyAddress(dict_ofMatchedLocations):

    dic_sortedOnScore = sorted(dict_ofMatchedLocations, key=lambda i: (i['score'], i['location_len']), reverse=True)

    for sk in dic_sortedOnScore:
        return sk
        break

    # return None


def observeLocation(provided_address, individual_key):

    if individual_key.get('locality').upper() in provided_address.upper():
        return len(individual_key.get('locality').upper())
    else:
        return -1


if __name__ == "__main__":
    main()

#
# def observePostCodes(provided_address, individual_key):
#     dict = {}
#
#     if individual_key.get('postcode').upper() in provided_address.upper():
#         dict['postcode'] = individual_key.get('postcode').upper()
#         return dict
#
#
# def observeState(provided_address, individual_key):
#     dict = {}
#
#     if individual_key.get('state').upper() in provided_address.upper():
#         dict['state'] = individual_key.get('state').upper()
#         return dict
#
#
# def createHash(to_hash):
#
#     b = to_hash.get('locality').upper().encode('utf-8')
#
#     hash_object = hashlib.md5(b)
#
#     return hash_object.hexdigest()

