# https://pysimplegui.readthedocs.io/en/latest/
from random import randint
# Threading Ideas: https://pysimplegui.trinket.io/demo-programs#/multi-threaded/multi-threaded-long-task-simple

import PySimpleGUI as sg
from Locality.Locality import Locality
from fileHandler import *
import ScreenDetails as sd


sd = sd.ScreenDetails().monitor_dictionary
print(sd)

# ------ Make the Table Data ------
DATA_GRID_COL_HEADINGS = ('','')
DATA_GRID_MAX_ROWS = 0
DATA_GRID_MAX_COLS = len(DATA_GRID_COL_HEADINGS)
data = [[j for j in range(DATA_GRID_MAX_COLS)] for i in range(DATA_GRID_MAX_ROWS)]
headings = list(DATA_GRID_COL_HEADINGS) # [str(data[0][x]) for x in range(len(data[0]))]

# I am considering to deprecate this component.
COL_HEADINGS = ('', '')

lb_action_to_apply = ('Full Address -> [Suburb],[State],[Postcode]','')

form_width = 120


""" 
This module initiates the current app. 

    Gui ->  no knowlege of business rules or other layers.

"""

# global visible_for_debug
visible_for_debug = True

debug_font = ("courier", 10)

tempFile = "I:\git\WordToExcel\Data\\20200602\\"




def updateStatusBar(window, message):
    window.FindElement( '_STATUSBAR_').Update(message + '\n', append=True, autoscroll=True)

def updateEventDisplayBar(window, message):
    window.FindElement('_EVENTDISPLAYBAR_').Update(message, append=False, autoscroll=False)



# ------ Column Definition ------ #

# Colour options: https://user-images.githubusercontent.com/46163555/71361827-2a01b880-2562-11ea-9af8-2c264c02c3e8.jpg
sg.ChangeLookAndFeel('Dark Blue 3')

# ------ Menu Definition ------ #
menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
            ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Help', '&About...'], ]

table = sg.Table(
        values=data[1:][:],
        headings=headings,
        max_col_width=25,
        background_color='lightblue',
        auto_size_columns=False,
        display_row_numbers=True,
        justification='left',
        num_rows=20,
        alternating_row_color='gray',
        key='_DATATABLE_'
        # tooltip='This is a table'
    )
layout = [
    [sg.Menu(menu_def, tearoff=False)]   ,
    [
        sg.Text('1. TESTING CODE ONY ----------')
    ],
    [sg.Text('_' * form_width)],

    [
        #https://pypi.org/project/PySimpleGUI/4.0.0/
        sg.Input(key='_FILEBROWSE_', enable_events=True, visible=False),
        sg.Text('Source File:', size=(9, 1), auto_size_text=False, justification='right'),
        sg.InputText('please select a file to process',key='_FILETOPROCESS_', text_color='gray', size=(98, 1)),
        sg.FileBrowse(
                        button_text="Browse",
                        file_types=(('CSV Files', '*.csv'), ('TXT Files', '*.txt'), ('All Files', '*.*')),
                        initial_folder=tempFile,
                        target='_FILEBROWSE_'
                    )
    ],

    [sg.Text('_' * form_width)],
    [
        sg.Frame('Column Headings (deprecate)',[[sg.Listbox(key='_COLUMNHEADINGS_', values=COL_HEADINGS, size=(30, len(COL_HEADINGS)))]], title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='')
        ,
        sg.Frame('Action to Apply',[[sg.Listbox(values=lb_action_to_apply, size=(form_width-40, len(lb_action_to_apply)))]], title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='')
    ],
    [sg.Text('_' * form_width)],

    [sg.Submit(key='_SUBMIT_', tooltip=''), sg.Cancel()],

    # to update: https://github.com/PySimpleGUI/PySimpleGUI/issues/1307
    [table],

    [sg.Multiline( key='_STATUSBAR_', size=(110, 5), auto_size_text=False, text_color='white', background_color='lightslategray', visible=visible_for_debug, font=debug_font )],
    [sg.Multiline( key='_EVENTDISPLAYBAR_', size=(110, 2), auto_size_text=False, text_color='white', background_color='lightslategray', visible=visible_for_debug, font=debug_font)],

]


# https://github.com/PySimpleGUI/PySimpleGUI/issues/850
window = sg.Window('A whole new world!').Layout(layout)

#https://stackoverflow.com/questions/55515627/pysimplegui-call-a-function-when-pressing-button
# While Loop might not be necessary.
while True:

    event, values = window.Read()

    if event is not None:
        updateEventDisplayBar(window, 'event name: ' + event)
        # updateEventDisplayBar(window, json.dumps(values))

    # This makes the app stop when you press X (close)
    elif event is None:
        break

    if event == '_FILEBROWSE_':
        # TODO: Test that an acutal File was provided

        file_name_and_path = values.get('_FILEBROWSE_')


        if len(file_name_and_path) > 0:
            window.FindElement('_FILETOPROCESS_').Update(text_color='black')
            window.FindElement('_FILETOPROCESS_').Update(file_name_and_path)

            h = fileHandler(file_name_and_path)

            DATA_GRID_COL_HEADINGS = (h.column_headings)

            window.FindElement('_COLUMNHEADINGS_').Update(values=DATA_GRID_COL_HEADINGS)
            window.FindElement('_COLUMNHEADINGS_').set_size((30, len(DATA_GRID_COL_HEADINGS)))

            updateStatusBar(window, 'Column Headings : ' + ', '.join(DATA_GRID_COL_HEADINGS))


            DATA_GRID_MAX_COLS = len(h.column_headings)
            DATA_GRID_MAX_ROWS = len(h.data_list)

            print(DATA_GRID_MAX_ROWS)
            print(DATA_GRID_MAX_COLS, ':', DATA_GRID_COL_HEADINGS)

            print(h.data_list)

            data = [
                [j for j in range(DATA_GRID_MAX_COLS)]
                for i in range(DATA_GRID_MAX_ROWS)
            ]
            headings = list(DATA_GRID_COL_HEADINGS)  # [str(data[0][x]) for x in range(len(data[0]))]

            # data = list(h.data_list)
            # list = []
            # for n in h.data_list:
            # for key, value in h.data_list:
            #     temp = [key, value]
            #     print(temp)
            #     list.append(temp)

            # headings = list(h.column_headings)

    # but probably even better is this! -> https://github.com/PySimpleGUI/PySimpleGUI/issues/845


            # and
# https://www.reddit.com/r/PySimpleGUI/comments/erlssi/multiple_window_change_active_loop/
#             for window in self.open_windows:
#                 closed = window.run()
#                 if closed:
#                     self.open_windows.remove(window)

            # window.FindElement('_DATATABLE_').Update(visible=True)
            window.FindElement('_DATATABLE_').Update(values = data)
            # window.FindElement('_DATATABLE_').Update(headings=headings)

            # window.FindElement('_DATAGRID_').set_size((800, 110))

        else:
            window.FindElement('_FILETOPROCESS_').Update(text_color='gray')
            window.FindElement('_FILETOPROCESS_').Update('please select a file to process')


    elif event == '_SUBMIT_' :
        updateStatusBar(window, 'STUB: With the file name in mind, process each line...')
        l = Locality(window, file_name_and_path, "ClientAddress")

        # print(l.data_list)
        # print(l.time_to_execute_seconds)

        updateStatusBar(window, 'Completed processing : ' + str(l.time_to_execute_seconds))


        # 1. Need our list of headings. they are used for the array to be created.


window.Close()