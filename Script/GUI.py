# https://pysimplegui.readthedocs.io/en/latest/
# Threading Ideas: https://pysimplegui.trinket.io/demo-programs#/multi-threaded/multi-threaded-long-task-simple
import PySimpleGUI as sg
import csv

# in house created code reference

from DataClensing.Locality import Locality
from applicationSettings import Configurations as config
from ext.fileHandler import *

app_config = config.Configurations()

# Global Variables -> Do i store them here or in
DATA_GRID_NESTED_LIST = []   # Represents the full Data pulled back from the 'file'

DATA_GRID_COL_HEADINGS = []  # connects to ListBox: _COLUMN_HEADINGS_
COLUMN_RENAME_LIST = [] # connects to ListBox: _COLUMN_RENAME_HEADINGS_
COLUMN_DATATYPE_LIST = [] # connects to ListBox: _COLUMN_DATATYPE_
COLUMN_ACTION_LIST = [] # connects to ListBox: _COLUMN_ACTION_

file_name_and_path = ""
selected_column = ""


# TODO: Relative Referencing required.
# tempFile = "I:\git\WordToExcel\Data\\20200602\\"
tempFile = "B:\/Users\wooda01.ADMINSRVAD\git\Applications\DataRepository\Data"

def updateStatusBar(window, message, override_previous):
    if override_previous == True:
        window.FindElement('_STATUSBAR_').Update(message + '\n', append=False, autoscroll=True)
    else:
        window.FindElement('_STATUSBAR_').Update(message + '\n', append=True, autoscroll=True)


def updateEventDisplayBar(window, message, override_previous):
    if override_previous == True:
        window.FindElement('_EVENTDISPLAYBAR_').Update(message, append=False, autoscroll=False)
    else:
        window.FindElement('_EVENTDISPLAYBAR_').Update(message, append=False, autoscroll=False)


# ------ Column Definition ------ #
# Colour options: https://user-images.githubusercontent.com/46163555/71361827-2a01b880-2562-11ea-9af8-2c264c02c3e8.jpg
sg.ChangeLookAndFeel('Dark Blue 3')

# ------ Menu Definition ------ #
menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
            ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Help', '&About...'], ]

command_button_size = (15, 1)

layout = [
    [sg.Menu(menu_def, tearoff=False)],
    # [
    #     sg.Text(
    #         '1. Select the file to process.\n2. Select the column to deidentify. \n3. Select the method to deidentify.'
    #         '\n4. Select the output file location.')
    # ],
    [sg.Text('_' * app_config.form_width)],

    [
        # https://pypi.org/project/PySimpleGUI/4.0.0/
        sg.Input(key='_FILEBROWSE_', enable_events=True, visible=False),
        sg.Text('Source File:', size=(9, 1), auto_size_text=False, justification='right'),
        sg.InputText('please select a file to process', key='_FILETOPROCESS_', text_color='gray', size=(98, 1)),
        sg.FileBrowse(
            button_text="Browse",
            file_types=(('CSV Files', '*.csv'), ('TXT Files', '*.txt'), ('All Files', '*.*')),
            initial_folder=tempFile,
            target='_FILEBROWSE_'
        )
    ],
    [sg.Text('_' * app_config.form_width)],

    [

        sg.Frame('Column Headings',
                 [[sg.Listbox(key='_COLUMN_HEADINGS_', enable_events=True, values=app_config.column_heading_list,  size=(30, len(app_config.column_heading_list)))]],
                 title_color='black',  relief=sg.RELIEF_SUNKEN, tooltip='')
        ,

        sg.Frame('Rename Column',
                 [[sg.Listbox(key='_COLUMN_RENAME_HEADINGS_', enable_events=True, values=app_config.column_heading_list,  size=(30, len(app_config.column_heading_list)))]],
                 title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='')

        ,
        sg.Frame('DataType Column',
                 [[sg.Listbox(key='_COLUMN_DATATYPE_', enable_events=True, values=app_config.column_heading_list, size=(30, len(app_config.column_heading_list)))]],
                 title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='')
        ,
        sg.Frame('Action to Apply on Column',
                 [[sg.Listbox(key='_COLUMN_ACTION_', enable_events=True, values=app_config.column_heading_list, size=(30, len(app_config.column_heading_list)))]],
                 title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='')

    ],

    [
    sg.Frame('Select Column',
        [[sg.InputCombo(values='', key='_COMBO_COLUMNNAME_', size=(30,1) )]],
             title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='')
    ,
    sg.Frame('Rename Column',
        [[sg.InputText( key='_INPUT_COLUMN_RENAME_',size=(30,1) )]],
             title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='')
    ,
    sg.Frame('Select DataType',
        [[sg.InputCombo(values=app_config.combo_datatype_list, key='_COMBO_DATATYPE_',size=(30,1) )]],
             title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='')
    ,
    sg.Frame('Select Action',
        [[sg.InputCombo(values=app_config.combo_action_list, key='_COMBO_ACTION_',size=(30,1) )]],
        title_color = 'black', relief = sg.RELIEF_SUNKEN, tooltip = '')
    ],
    [sg.Text('_' * app_config.form_width)],

    [
        sg.Submit(key='_SUBMIT_', tooltip='', size=command_button_size),
        sg.Cancel(size=command_button_size),
        sg.Submit("View Data", key='_VIEWDATA_', tooltip='', size=command_button_size),
        sg.Submit("Save Data", key='_SAVEDATA_', tooltip='', size=command_button_size)
    ],

    [sg.Multiline(key='_STATUSBAR_', size=(110, 5), auto_size_text=False, text_color='white',
                  background_color='lightslategray', visible=app_config.controls_visible_for_debug, font=app_config.controls_debug_font)],
    [sg.Multiline(key='_EVENTDISPLAYBAR_', size=(110, 2), auto_size_text=False, text_color='white',
                  background_color='lightslategray', visible=app_config.controls_visible_for_debug, font=app_config.controls_debug_font)],

]

# https://github.com/PySimpleGUI/PySimpleGUI/issues/850
window = sg.Window('Data Cleansing').Layout(layout)

# https://stackoverflow.com/questions/55515627/pysimplegui-call-a-function-when-pressing-button
# While Loop might not be necessary.
while True:

    event, values = window.Read()
    # print(INITIAL_LOAD)
    if event is not None:
        # updateEventDisplayBar(window, 'event name: ' + event, False)
        updateEventDisplayBar(window, json.dumps(values), False)

    # This makes the app stop when you press X (close)
    elif event is None:
        break

    if event == '_FILEBROWSE_':

        # This is an intial load for each file.

        file_name_and_path = values.get('_FILEBROWSE_')

        if len(file_name_and_path) > 0:
            window.FindElement('_FILETOPROCESS_').Update(text_color='black')
            window.FindElement('_FILETOPROCESS_').Update(file_name_and_path)

            file_containing_data = fileHandler(file_name_and_path)

            DATA_GRID_COL_HEADINGS = file_containing_data.column_headings
            DATA_GRID_NESTED_LIST = file_containing_data.data_nested_list

            window.FindElement('_COLUMN_HEADINGS_').Update(values=DATA_GRID_COL_HEADINGS)
            window.FindElement('_COLUMN_HEADINGS_').set_size((30, len(DATA_GRID_COL_HEADINGS))) #ie, configure Height to the number of Column Headers

            COLUMN_RENAME_LIST = [None] * len(DATA_GRID_COL_HEADINGS) # connects to ListBox: _COLUMN_RENAME_HEADINGS_
            COLUMN_DATATYPE_LIST = [None] * len(DATA_GRID_COL_HEADINGS) # connects to ListBox: _COLUMN_DATATYPE_
            COLUMN_ACTION_LIST = [None] * len(DATA_GRID_COL_HEADINGS)  # connects to ListBox: _COLUMN_ACTION_

            window.FindElement('_COLUMN_RENAME_HEADINGS_').Update(values=COLUMN_RENAME_LIST)
            window.FindElement('_COLUMN_RENAME_HEADINGS_').set_size((30, len(COLUMN_RENAME_LIST))) #ie, configure Height to the number of Column Headers

            window.FindElement('_COLUMN_DATATYPE_').Update(values=COLUMN_DATATYPE_LIST)
            window.FindElement('_COLUMN_DATATYPE_').set_size((30, len(COLUMN_DATATYPE_LIST))) #ie, configure Height to the number of Column Headers

            window.FindElement('_COLUMN_ACTION_').Update(values=COLUMN_ACTION_LIST)
            window.FindElement('_COLUMN_ACTION_').set_size((30, len(COLUMN_ACTION_LIST))) #ie, configure Height to the number of Column Headers


            window.FindElement('_COMBO_COLUMNNAME_').Update(values=DATA_GRID_COL_HEADINGS)

            updateStatusBar(window, 'Column Headings : ' + ', '.join(DATA_GRID_COL_HEADINGS), False)

        else:
            window.FindElement('_FILETOPROCESS_').Update(text_color='gray')
            window.FindElement('_FILETOPROCESS_').Update('please select a file to process')

    elif event == '_SUBMIT_':

        file_name_and_path = values.get('_FILEBROWSE_')

        if file_name_and_path != "":

            if (selected_column == ""):
                print('Column heading not selected! ')  # do this first prior to continuing.

            updateStatusBar(window, 'STUB: With the file name in mind, process each line...', False)

            l = Locality(window, DATA_GRID_COL_HEADINGS, DATA_GRID_NESTED_LIST, selected_column)
            DATA_GRID_NESTED_LIST = l.data_nested_list

            updateStatusBar(window, 'Completed processing : ' + str(l.time_to_execute_seconds), False)

            window.FindElement('_COLUMN_HEADINGS_').Update(values=DATA_GRID_COL_HEADINGS)
            window.FindElement('_COLUMN_HEADINGS_').set_size((30, len(DATA_GRID_COL_HEADINGS)))

            # d = Dates(window, DATA_GRID_COL_HEADINGS, DATA_GRID_NESTED_LIST, selected_column)
            # We need a way to deal with a Data set, rather than always opening the file.

    elif event == '_COLUMN_HEADINGS_':  # if a list item is chosen

        for selected in values['_COLUMN_HEADINGS_']:
            selected_column = selected
            print(selected)

            # UPDATE THIS -> https://quabr.com/61170768/how-do-i-use-the-value-in-a-list-with-combo-pysimplegui
            # window.FindElement('_COMBO_COLUMNNAME_').Update((30, len(DATA_GRID_COL_HEADINGS)))



            updateStatusBar(window, 'Selected Heading : ' + str(selected_column), False)
            break


    elif event == '_VIEWDATA_':

        if file_name_and_path != "":
            from DataTablePopUp import *

            DataTablePopUp(data_table_headings=DATA_GRID_COL_HEADINGS, data_table_data=DATA_GRID_NESTED_LIST,
                           data_description=file_containing_data.file_name)

            pass

    elif event == '_SAVEDATA_':

        # TODO : Convert this to relative referencing. This folder is a natural folder.
        example = "I:\git\WordToExcel\Data\\20200615\\t.csv"


        with open("I:\git\WordToExcel\Data\\20200615\\temp.csv", "w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow(DATA_GRID_COL_HEADINGS)

            for record in DATA_GRID_NESTED_LIST:
                # print(record)
                writer.writerow(record)

        pass

window.Close()
