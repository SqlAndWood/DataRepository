#! Python 3.4
"""
https://gist.github.com/Yagisanatode/0d1baad4e3a871587ab1
"""
import os
from csv import DictReader
import AddressFinder

from collections import OrderedDict
import csv

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

# window = tk.Tk() -> Display a new window.
root = Tk(  )

# column_to_resolve = "ClientAddress"
column_to_resolve = "RelContactDetails"

action_to_perform = "AddressFinder"


#This is where we lauch the file manager bar.
def OpenFile():
    mapping_folder_path = os.path.abspath(os.path.dirname("."))

    mapping_folder_path = "I:\git\WordToExcel\Data\\20200602"

    file_name_and_path = askopenfilename(initialdir=mapping_folder_path,
                           filetypes =(("Text File", "*.csv"),("All Files","*.*")),
                           title = "Choose a file."
                           )

    label = ttk.Label(root, text=file_name_and_path, foreground="black", font=("Helvetica", 12))
    label.pack()


    file_name = file_name_and_path [len(mapping_folder_path) + 1 :len(file_name_and_path)]

    #Using try in case user types in unknown file or closes without choosing a file.
    try:
        print('about to process data')
        CreateData(file_name, file_name_and_path, mapping_folder_path)
        print('completed with the data')
    except:
        print("No file exists")



#currently for Address only.
def CreateData(file_name,file_name_and_path, mapping_folder_path):

    new_file_name = file_name [ :len(file_name)-4] + "_Address_DI.csv"
    print(file_name , ' has columns ' , column_to_resolve)

    with open(file_name_and_path, 'r') as file_to_use:

        print('file opened successfully. Processing Data. Please wait.')
        csv_dict_reader = DictReader(file_to_use)

        column_names = csv_dict_reader.fieldnames

        # https://thispointer.com/python-read-a-csv-file-line-by-line-with-or-without-header/

        with open(mapping_folder_path + '//' + new_file_name, 'w', newline='') as csvfile:
            # print('Saving new data to: ', mapping_folder_path + '//' + new_file_name)

            fieldnames = column_names
            fieldnames.append('locality')
            fieldnames.append('state')
            fieldnames.append('postcode')

            # print(fieldnames)

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in csv_dict_reader:
                # print(row[column_to_resolve])
                # print(type(row))


                la = AddressFinder.resolveAddress(row[column_to_resolve])

                # print(la)

                if la is not None:
                    row['locality'] = la['locality']
                    row['state'] = la['state']
                    row['postcode'] = la['postcode']

                else:
                    row['locality'] = ""
                    row['state'] = ""
                    row['postcode'] = ""

                # print(row)
                writer.writerow(row)


            # print('job done')



Title = root.title("File Opener")
label = ttk.Label(root, text="", foreground="red", font=("Helvetica", 16))
label.pack()

# Menu Bar

menu = Menu(root)
root.config(menu=menu)

file = Menu(menu)

file.add_command(label='Open', command=OpenFile)
file.add_command(label='Exit', command=lambda: exit())

menu.add_cascade(label='File', menu=file)

root.mainloop()

