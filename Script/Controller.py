import pandas as pd
import os
import time
import hashlib #hashing algorithm

from com import FileWalker, JSONReader

def main():
    start_time = time.time()

    dict_location = loadDictionary()
    matchAddress(dict_location)


    print("--- %s seconds ---" % (time.time() - start_time))
# 3:41 sec for Parts 1 -3




def loadDictionary():
    debug = False
    pd.set_option("display.max_rows", 30, "display.max_columns", None)

    docxLocation = "..\Data\\"
    pdfLocation = "..\Data\\"

    mapping_folder_path = "..\mapping\\"
    mapping_file_name = 'australian_postcodes.json'

    output_to_ss = "..\Data\Output\\"

    # mappings are important for how to process the file and associated sections
    mapping_folder_path = os.path.abspath(os.path.dirname(docxLocation))
    dict_location = JSONReader.readJSON(mapping_folder_path, mapping_file_name)

    #this may be of use at a later date
    df = JSONReader.readJSONtoDataFrame(mapping_folder_path, mapping_file_name)

    return dict_location

# This is a fuzzy adress match. Only one address is to be matched, as the most likely match.
# matching the incorrect address is not a key issue here.

def matchAddress(dict_location):


    # print(df.locality.to_string(index=False))
    # print(df.postcode.to_string(index=False))

    # print (  df[['id','locality', 'postcode', 'state', 'lat', 'long']] )

    provided_address = "8 Dighton St, PORT AUGUSTA WEST SA 5700  (C3MS)"

    count = 0
    records_found = 0
    score = 0

    dic_identified = {}

    for individual_key in dict_location:

        count += 1

        individual_key['location_len'] = observeLocation(provided_address, individual_key)

        opc = observePostCodes(provided_address, individual_key)
        ost = observeState(provided_address, individual_key)

        # temporary while I figure out how I'd like the algorithm to be.
        if individual_key.get('locality').upper() in provided_address.upper() and individual_key.get('postcode') in provided_address.upper():
            score += 1

            # locality = n.get('locality')
            # postcode = n.get('postcode')
            # id = n.get('id')
            # state = n.get('state')
            # lat = n.get('lat')
            # long = n.get('long')



        if score > 0:
            print('c: ', count, ' l:' , individual_key)

            records_found += 1
            score = 0
            dic_identified[count] = individual_key


    print('Records found: ', records_found)

    sorted_keys = sorted (dic_identified, key=lambda x: (dic_identified[x]['location_len']) , reverse=True )


    for sk in sorted_keys:

        most_likely = dic_identified[sk]
        break

    print(most_likely)



def observeLocation(provided_address, individual_key):

    if individual_key.get('locality').upper() in provided_address.upper():

        # dict['locality_len'] = len(individual_key.get('locality').upper())

        return len(individual_key.get('locality').upper())




def observePostCodes(provided_address, individual_key):
    dict = {}

    if individual_key.get('postcode').upper() in provided_address.upper():
        dict['postcode'] = individual_key.get('postcode').upper()
        return dict


def observeState(provided_address, individual_key):
    dict = {}

    if individual_key.get('state').upper() in provided_address.upper():
        dict['state'] = individual_key.get('state').upper()
        return dict


def createHash(to_hash):

    b = to_hash.get('locality').upper().encode('utf-8')

    hash_object = hashlib.md5(b)

    return hash_object.hexdigest()


def mostLikelyLocation(Observed):
    dict = {}



    # for n in Observed:
    #     print(n.get('locality_len'))
    #     print(n)

    # for key, value in Observed.items():
    #     print(key, '->', value)


if __name__ == "__main__":
    main()