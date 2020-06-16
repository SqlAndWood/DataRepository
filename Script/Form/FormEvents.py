import csv
import json

from DataClensing.Locality import Locality
from DataTablePopUp import *
from ext import fileHandler as fh


class FormEvents:

    # fh = Configurations()
    def __init__(self, window):

        self.window = window

        self.file_name_and_path = ""
        self.selected_column = ""
        self.InstantiateForm()

        # Global Variables -> Do i store them here or in app_config?
        # this now needs to be fixed.. or not. not sure how Python does tis part.
        # DATA_GRID_NESTED_LIST = []  # Represents the full Data pulled back from the 'file'
        # DATA_GRID_COL_HEADINGS = []  # connects to ListBox: _COLUMN_HEADINGS_
        # COLUMN_RENAME_LIST = []  # connects to ListBox: _COLUMN_RENAME_HEADINGS_
        # COLUMN_DATATYPE_LIST = []  # connects to ListBox: _COLUMN_DATATYPE_
        # COLUMN_ACTION_LIST = []  # connects to ListBox: _COLUMN_ACTION_

    def updateStatusBar(self, message, override_previous):
        if override_previous == True:
            self.window.FindElement('_STATUSBAR_').Update(message + '\n', append=False, autoscroll=True)
        else:
            self.window.FindElement('_STATUSBAR_').Update(message + '\n', append=True, autoscroll=True)

    def updateEventDisplayBar(self, message, override_previous):
        if override_previous == True:
            self.window.FindElement('_EVENTDISPLAYBAR_').Update(message, append=False, autoscroll=False)
        else:
            self.window.FindElement('_EVENTDISPLAYBAR_').Update(message, append=False, autoscroll=False)

    def InstantiateForm(self):
        # https://stackoverflow.com/questions/55515627/pysimplegui-call-a-function-when-pressing-button
        # While Loop might not be necessary.
        while True:

            event, values = self.window.Read()
            # print(INITIAL_LOAD)
            if event is not None:
                # updateEventDisplayBar(window, 'event name: ' + event, False)
                self.updateEventDisplayBar(json.dumps(values), False)

            # This makes the app stop when you press X (close)
            elif event is None:
                break

            if event == '_FILEBROWSE_':

                # This is an intial load for each file.

                self.file_name_and_path = values.get('_FILEBROWSE_')

                if len(self.file_name_and_path) > 0:
                    self.window.FindElement('_FILETOPROCESS_').Update(text_color='black')
                    self.window.FindElement('_FILETOPROCESS_').Update(self.file_name_and_path)

                    file_containing_data = fh.fileHandler(self.file_name_and_path)

                    # this should be a stand alone Function.. re working.
                    DATA_GRID_COL_HEADINGS = file_containing_data.column_headings
                    DATA_GRID_NESTED_LIST = file_containing_data.data_nested_list

                    self.window.FindElement('_COLUMN_HEADINGS_').Update(values=DATA_GRID_COL_HEADINGS)
                    self.window.FindElement('_COLUMN_HEADINGS_').set_size(
                        (30, len(DATA_GRID_COL_HEADINGS)))  # ie, configure Height to the number of Column Headers

                    COLUMN_RENAME_LIST = DATA_GRID_COL_HEADINGS  # [''] * len(DATA_GRID_COL_HEADINGS)  # connects to ListBox: _COLUMN_RENAME_HEADINGS_
                    COLUMN_DATATYPE_LIST = [''] * len(DATA_GRID_COL_HEADINGS)  # connects to ListBox: _COLUMN_DATATYPE_
                    COLUMN_ACTION_LIST = [''] * len(DATA_GRID_COL_HEADINGS)  # connects to ListBox: _COLUMN_ACTION_

                    self.window.FindElement('_COLUMN_RENAME_HEADINGS_').Update(values=COLUMN_RENAME_LIST)
                    self.window.FindElement('_COLUMN_RENAME_HEADINGS_').set_size(
                        (30, len(COLUMN_RENAME_LIST)))  # ie, configure Height to the number of Column Headers

                    self.window.FindElement('_COLUMN_DATATYPE_').Update(values=COLUMN_DATATYPE_LIST)
                    self.window.FindElement('_COLUMN_DATATYPE_').set_size(
                        (30, len(COLUMN_DATATYPE_LIST)))  # ie, configure Height to the number of Column Headers

                    self.window.FindElement('_COLUMN_ACTION_').Update(values=COLUMN_ACTION_LIST)
                    self.window.FindElement('_COLUMN_ACTION_').set_size(
                        (30, len(COLUMN_ACTION_LIST)))  # ie, configure Height to the number of Column Headers

                    self.window.FindElement('_COMBO_COLUMNNAME_').Update(values=DATA_GRID_COL_HEADINGS)

                    self.updateStatusBar('Column Headings : ' + ', '.join(DATA_GRID_COL_HEADINGS), False)

                else:
                    self.window.FindElement('_FILETOPROCESS_').Update(text_color='gray')
                    self.window.FindElement('_FILETOPROCESS_').Update('please select a file to process')

            elif event == '_SUBMIT_':

                self.file_name_and_path = values.get('_FILEBROWSE_')

                if self.file_name_and_path != "":

                    if (self.selected_column == ""):
                        print('Column heading not selected! ')  # do this first prior to continuing.

                    self.updateStatusBar('STUB: With the file name in mind, process each line...', False)

                    l = Locality(self.window, DATA_GRID_COL_HEADINGS, DATA_GRID_NESTED_LIST, self.selected_column)
                    DATA_GRID_NESTED_LIST = l.data_nested_list

                    self.updateStatusBar('Completed processing : ' + str(l.time_to_execute_seconds), False)

                    self.window.FindElement('_COLUMN_HEADINGS_').Update(values=DATA_GRID_COL_HEADINGS)
                    self.window.FindElement('_COLUMN_HEADINGS_').set_size((30, len(DATA_GRID_COL_HEADINGS)))

                    # d = Dates(window, DATA_GRID_COL_HEADINGS, DATA_GRID_NESTED_LIST, self.selected_column)
                    # We need a way to deal with a Data set, rather than always opening the file.

            elif event == '_COLUMN_HEADINGS_':  # if a list item is chosen
                i = 0

                for v in DATA_GRID_COL_HEADINGS:
                    self.selected_column = values.get('_COLUMN_HEADINGS_')[0]
                    if v == self.selected_column:
                        # https://quabr.com/61170768/how-do-i-use-the-value-in-a-list-with-combo-pysimplegui
                        self.window.FindElement('_COMBO_COLUMNNAME_').Update(value=self.selected_column)
                        self.window.FindElement('_INPUT_COLUMN_RENAME_').Update(value=COLUMN_RENAME_LIST[i])
                        self.window.FindElement('_COMBO_DATATYPE_').Update(value=COLUMN_DATATYPE_LIST[i])
                        self.window.FindElement('_COMBO_ACTION_').Update(value=COLUMN_ACTION_LIST[i])

                        self.updateStatusBar('Selected Heading : ' + str(self.selected_column), False)
                        break

                    i += 1


            elif event == '_COMBO_COLUMNNAME_':  # Update associated collumn on click.
                i = 0
                for v in DATA_GRID_COL_HEADINGS:
                    if v == values.get('_COMBO_COLUMNNAME_'):
                        self.window.FindElement('_COLUMN_HEADINGS_').Update(set_to_index=i)
                        break
                    i += 1

            elif event == '_VIEWDATA_':

                if self.file_name_and_path != "":
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

            elif event == '_UPDATE_COLUMN_DEFINITION_':

                i = 0
                for v in DATA_GRID_COL_HEADINGS:
                    if v == values.get('_COMBO_COLUMNNAME_'):
                        rename = values.get('_INPUT_COLUMN_RENAME_')
                        data_type = values.get('_COMBO_DATATYPE_')
                        action_to_perform = values.get('_COMBO_ACTION_')

                        COLUMN_RENAME_LIST[i] = rename  # connects to ListBox: _COLUMN_RENAME_HEADINGS_
                        COLUMN_DATATYPE_LIST[i] = data_type  # connects to ListBox: _COLUMN_DATATYPE_
                        COLUMN_ACTION_LIST[i] = action_to_perform  # connects to ListBox: _COLUMN_ACTION_

                        self.window.FindElement('_COLUMN_RENAME_HEADINGS_').Update(values=COLUMN_RENAME_LIST)

                        self.window.FindElement('_COLUMN_DATATYPE_').Update(values=COLUMN_DATATYPE_LIST)

                        self.window.FindElement('_COLUMN_ACTION_').Update(values=COLUMN_ACTION_LIST)

                        self.window.FindElement('_COMBO_COLUMNNAME_').Update(values=DATA_GRID_COL_HEADINGS)

                        break
                    i += 1

                pass

        self.window.Close()
