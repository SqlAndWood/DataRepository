import pandas as pd
import os
import time

from com import FileWalker, JSONReader

def main():
    debug = False
    pd.set_option("display.max_rows", 30, "display.max_columns", None)

    start_time = time.time()

    docxLocation = "..\Data\\"
    pdfLocation = "..\Data\\"

    mapping_folder_path = "..\mapping\\"
    mapping_file_name = 'australian_postcodes.json'

    output_to_ss = "..\Data\Output\\"

    # mappings are important for how to process the file and associated sections
    mapping_folder_path = os.path.abspath(os.path.dirname(docxLocation))
    mappings = JSONReader.readJSON(mapping_folder_path, mapping_file_name)

    df = JSONReader.readJSONtoDataFrame(mapping_folder_path, mapping_file_name)

    # print(df.locality.to_string(index=False))
    # print(df.postcode.to_string(index=False))

    # print (  df[['id','locality', 'postcode', 'state', 'lat', 'long']] )

    t = "50 Dotterel Dve Semaphore Park SA 5019"
    count = 0
    records_found = 0

    flag = False
    #
    for n in mappings:
        # print(n)
        count += 1

        if n.get('locality').upper() in t.upper() and  n.get('postcode') in t.upper():
            flag = True
            # locality = n.get('locality')
            # postcode = n.get('postcode')
            # id = n.get('id')
            # state = n.get('state')
            # lat = n.get('lat')
            # long = n.get('long')

        if flag:
            print('c: ', count, ' l:' , n)
            flag = False
            records_found += 1
    #
    # print(count)
    print('Records found: ', records_found)
    print("--- %s seconds ---" % (time.time() - start_time))
# 3:41 sec for Parts 1 -3









if __name__ == "__main__":
    main()