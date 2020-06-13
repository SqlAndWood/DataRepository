import csv
# This module will not execute, it is just old code to 'save' using the DictWriter
new_file_name = file_name [ :len(file_name)-4] + "_Address_DI.csv"

with open(mapping_folder_path + '//' + new_file_name, 'w', newline='') as csvfile:

    writer = csv.DictWriter(csvfile, fieldnames="fieldnames")
    writer.writeheader()

    writer.writerow('the dtails found')