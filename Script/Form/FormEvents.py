import csv
import json
import time


from DataClensing.Locality import Locality
from DataTablePopUp import *
from ext import fileHandler as fh

# Great example of filtering on a list() : https://github.com/PySimpleGUI/PySimpleGUI/issues/1633
# new_values = [x for x in names if search in x]

class FormEvents:

    # fh = Configurations()
    def __init__(self, window):

        self.window = window
        self.file_name_and_path = ""

        self.selected_column_by_integer = 0

        # not being used yet. unsure if necessary at all.
        self.selected_column = ""

        # Global Variables -> Do i store them here or in app_config?
        # this now needs to be fixed.. or not. not sure how Python does tis part.
        self.DATA_GRID_NESTED_LIST = []  # Represents the full Data pulled back from the 'file'
        self.DATA_GRID_COL_HEADINGS = []  # connects to ListBox: _COLUMN_HEADINGS_
        self.COLUMN_RENAME_LIST = []  # connects to ListBox: _COLUMN_RENAME_HEADINGS_
        self.COLUMN_DATATYPE_LIST = []  # connects to ListBox: _COLUMN_DATATYPE_
        self.COLUMN_ACTION_LIST = []  # connects to ListBox: _COLUMN_ACTION_

        self.InstantiateForm()


    def updateStatusBar(self, message):
        self.window.FindElement('_STATUSBAR_').Update(message + '\n', append=False, autoscroll=True)

    def UpdateEventBar(self):
        self.updateStatusBar('event name: ' + self.event)
        self.updateStatusBar(json.dumps(self.values))


    def OpenFileAndDisplay(self):
        # This is an intial load for each file.
        start_time = time.time()

        self.file_name_and_path = self.values.get('_FILEBROWSE_')

        if len(self.file_name_and_path) > 0:
            self.window.FindElement('_FILETOPROCESS_').Update(text_color='black')
            self.window.FindElement('_FILETOPROCESS_').Update(self.file_name_and_path)

            self.file_containing_data = fh.fileHandler(self.file_name_and_path)

            # this should be a stand alone Function.. re working.
            self.DATA_GRID_COL_HEADINGS = self.file_containing_data.column_headings
            self.DATA_GRID_NESTED_LIST = self.file_containing_data.data_nested_list


            self.COLUMN_RENAME_LIST = self.DATA_GRID_COL_HEADINGS  # [''] * len(DATA_GRID_COL_HEADINGS)  # connects to ListBox: _COLUMN_RENAME_HEADINGS_
            self.COLUMN_DATATYPE_LIST = [''] * len(self.DATA_GRID_COL_HEADINGS)  # connects to ListBox: _COLUMN_DATATYPE_
            self.COLUMN_ACTION_LIST = [''] * len(self.DATA_GRID_COL_HEADINGS)  # connects to ListBox: _COLUMN_ACTION_

            self.UpdateListBoxes()


            self.window.FindElement('_COMBO_COLUMNNAME_').Update(values=self.DATA_GRID_COL_HEADINGS)

            self.window.FindElement('_INPUT_COLUMN_RENAME_').Update(value=self.COLUMN_RENAME_LIST[self.selected_column_by_integer])

            self.updateStatusBar('Column Headings : ' + ', '.join(self.DATA_GRID_COL_HEADINGS))

            self.HighlightAssociatedListBox()

        else:
            self.window.FindElement('_FILETOPROCESS_').Update(text_color='gray')
            self.window.FindElement('_FILETOPROCESS_').Update('please select a file to process')

        print("---Process file:  %s seconds ---" % (time.time() - start_time))

    def HighlightAssociatedListBox(self):
        start_time = time.time()
        self.window.FindElement('_COLUMN_HEADINGS_').Update(set_to_index=self.selected_column_by_integer)
        self.window.FindElement('_COLUMN_RENAME_HEADINGS_').Update(set_to_index=self.selected_column_by_integer)
        self.window.FindElement('_COLUMN_DATATYPE_').Update(set_to_index=self.selected_column_by_integer)
        self.window.FindElement('_COLUMN_ACTION_').Update(set_to_index=self.selected_column_by_integer)

        print("---HighlightAssociatedListBox:  %s seconds ---" % (time.time() - start_time))

    def IdentifyComboIndexSelected(self):
        start_time = time.time()
        # https://www.programiz.com/python-programming/methods/list/index  -> index = vowels.index('e')
        self.selected_column_by_integer = self.DATA_GRID_COL_HEADINGS.index(self.values.get('_COMBO_COLUMNNAME_'))

        print("---IdentifyComboIndexSelected:  %s seconds ---" % (time.time() - start_time))

    def IdentifyListBoxIndexSelected(self):
        start_time = time.time()
        # https://www.programiz.com/python-programming/methods/list/index  -> index = vowels.index('e')
        self.selected_column_by_integer = self.DATA_GRID_COL_HEADINGS.index(self.values.get('_COLUMN_HEADINGS_')[0])

        print("---IdentifyListBoxIndexSelected:  %s seconds ---" % (time.time() - start_time))

    def UpdateUserInputs(self):  #These are the three single line Inputs
        start_time = time.time()
        self.window.FindElement('_INPUT_COLUMN_RENAME_').Update(value=self.COLUMN_RENAME_LIST[self.selected_column_by_integer])
        self.window.FindElement('_COMBO_DATATYPE_').Update(value=self.COLUMN_DATATYPE_LIST[self.selected_column_by_integer])
        self.window.FindElement('_COMBO_ACTION_').Update(value=self.COLUMN_ACTION_LIST[self.selected_column_by_integer])

        print("---UpdateUserInputs:  %s seconds ---" % (time.time() - start_time))

    def UpdateListBoxes(self):
        start_time = time.time()
        self.window.FindElement('_COLUMN_HEADINGS_').Update(values=self.DATA_GRID_COL_HEADINGS)
        self.window.FindElement('_COLUMN_HEADINGS_').set_size((30, len(self.DATA_GRID_COL_HEADINGS)))  # ie, configure Height to the number of Column Headers

        self.window.FindElement('_COLUMN_RENAME_HEADINGS_').Update(values=self.COLUMN_RENAME_LIST)
        self.window.FindElement('_COLUMN_RENAME_HEADINGS_').set_size((30, len(self.COLUMN_RENAME_LIST)))  # ie, configure Height to the number of Column Headers

        self.window.FindElement('_COLUMN_DATATYPE_').Update(values=self.COLUMN_DATATYPE_LIST)
        self.window.FindElement('_COLUMN_DATATYPE_').set_size((30, len(self.COLUMN_DATATYPE_LIST)))  # ie, configure Height to the number of Column Headers

        self.window.FindElement('_COLUMN_ACTION_').Update(values=self.COLUMN_ACTION_LIST)
        self.window.FindElement('_COLUMN_ACTION_').set_size((30, len(self.COLUMN_ACTION_LIST)))  # ie, configure Height to the number of Column Headers

        print("---UpdateListBoxes:  %s seconds ---" % (time.time() - start_time))

    def UpdateAllThreeLists_KeyPressChangeEvent(self):
        start_time = time.time()
        self.COLUMN_RENAME_LIST[self.selected_column_by_integer] = self.values.get('_INPUT_COLUMN_RENAME_')  # connects to ListBox: _COLUMN_RENAME_HEADINGS_
        self.COLUMN_DATATYPE_LIST[self.selected_column_by_integer] = self.values.get('_COMBO_DATATYPE_')  # connects to ListBox: _COLUMN_DATATYPE_
        self.COLUMN_ACTION_LIST[self.selected_column_by_integer] =  self.values.get('_COMBO_ACTION_')  # connects to ListBox: _COLUMN_ACTION_

        print("---UpdateAllThreeLists_KeyPressChangeEvent:  %s seconds ---" % (time.time() - start_time))

    # this needs to be re-written and given to a different class.
    def SubmitDataForProcessing(self):

        self.file_name_and_path = self.values.get('_FILEBROWSE_')

        if self.file_name_and_path != "":

            if (self.selected_column == ""):
                print('Column heading not selected! ')  # do this first prior to continuing.

            self.updateStatusBar('STUB: With the file name in mind, process each line...')

            l = Locality(self.window, self.DATA_GRID_COL_HEADINGS, self.DATA_GRID_NESTED_LIST, self.selected_column)
            DATA_GRID_NESTED_LIST = l.data_nested_list

            self.updateStatusBar('Completed processing : ' + str(l.time_to_execute_seconds))

            self.window.FindElement('_COLUMN_HEADINGS_').Update(values=self.DATA_GRID_COL_HEADINGS)
            self.window.FindElement('_COLUMN_HEADINGS_').set_size((30, len(self.DATA_GRID_COL_HEADINGS)))

            # d = Dates(window, DATA_GRID_COL_HEADINGS, DATA_GRID_NESTED_LIST, self.selected_column)
            # We need a way to deal with a Data set, rather than always opening the file.


    def ViewDataViaPopUpWindow(self):
        if self.file_name_and_path != "":
            DataTablePopUp(data_table_headings=self.DATA_GRID_COL_HEADINGS, data_table_data=self.DATA_GRID_NESTED_LIST,
                           data_description=self.file_containing_data.file_name)


    def SaveDataTableToFile(self):
        # TODO : Convert this to relative referencing. This folder is a natural folder.
        with open("I:\git\WordToExcel\Data\\20200615\\temp.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.DATA_GRID_COL_HEADINGS)
            for record in self.DATA_GRID_NESTED_LIST:
                writer.writerow(record)


    def InstantiateForm(self):

        # https://stackoverflow.com/questions/55515627/pysimplegui-call-a-function-when-pressing-button
        # While Loop might not be necessary.
        while True:


            self.event, self.values = self.window.Read()

            if self.event is not None:
                # print("---NO EVENT:  %s seconds ---" % (time.time() - start_time))
                self.UpdateEventBar()

            # Action #1: Without a File browse, nothing else will occur.
            if self.event == '_FILEBROWSE_':
                self.OpenFileAndDisplay()

            # Action #2: A 'Column' must first be selected from the command button.
                # upon the user selecting from the command button, associated List Box Pos will be Highlighted.
                # variable: self.selected_column_by_integer  keeps track of the current selected posision
            elif self.event == '_COMBO_COLUMNNAME_':  # Update associated collumn on click.
                start_time = time.time()
                self.IdentifyComboIndexSelected()
                # this is an ambiguous function name; however I am returning the current list information to the Form fo rthe user to know what they have selected.
                self.UpdateUserInputs()
                self.HighlightAssociatedListBox()
                print("---COMBO Change:  %s seconds ---" % (time.time() - start_time))

            # Alternative Action #2, a User might accidently select from teh List Box itself. if they do, ...
            elif self.event == '_COLUMN_HEADINGS_':  # Update associated collumn on click.
                start_time = time.time()
                self.IdentifyListBoxIndexSelected()
                # this is an ambiguous function name; however I am returning the current list information to the Form fo rthe user to know what they have selected.
                self.UpdateUserInputs()
                self.HighlightAssociatedListBox()
                print("---Column Heading Change:  %s seconds ---" % (time.time() - start_time))

            # Action #3: The following three controls are updated with the same code.
               # Update the List Boxes with the provided details.
            elif self.event == '_INPUT_COLUMN_RENAME_' or self.event == '_COMBO_DATATYPE_' or self.event == '_COMBO_ACTION_' :
                start_time = time.time()
                self.UpdateAllThreeLists_KeyPressChangeEvent()

                # update everything that just changed.
                self.UpdateListBoxes()
                # this is an ambiguous function name; however I am returning the current list information to the Form fo rthe user to know what they have selected.
                self.UpdateUserInputs()
                self.HighlightAssociatedListBox()
                print("---Three over arching things chagned:  %s seconds ---" % (time.time() - start_time))

            # The very last step in the entire process. This is the Action shot.
            elif self.event == '_SUBMIT_':
                self.SubmitDataForProcessing()

            # at any time you may save the data you have compiled.
            elif self.event == '_SAVEDATA_':
                self.SaveDataTableToFile()

            # at any time, you may view the data you have compiled.
            elif self.event == '_VIEWDATA_':
                self.ViewDataViaPopUpWindow()

            # Allow the app to quit when you press X (close)
            elif self.event is None:
                break

        self.window.Close()



#  DEPRECATED CODE
#  def PopulateUserEntryUpdateControls(self):
#         # Considsering NOT Doing this.
#         i = 0
#
#         self.selected_column = self.values.get('_COMBO_COLUMNNAME_')[0]
#
#         for v in self.DATA_GRID_COL_HEADINGS:
#
#             if v == self.selected_column:
#
#                 self.selected_column_by_integer
#
#                 # https://quabr.com/61170768/how-do-i-use-the-value-in-a-list-with-combo-pysimplegui
#                 self.window.FindElement('_COMBO_COLUMNNAME_').Update(value=self.selected_column)
#                 self.window.FindElement('_INPUT_COLUMN_RENAME_').Update(value=self.COLUMN_RENAME_LIST[i])
#                 self.window.FindElement('_COMBO_DATATYPE_').Update(value=self.COLUMN_DATATYPE_LIST[i])
#                 self.window.FindElement('_COMBO_ACTION_').Update(value=self.COLUMN_ACTION_LIST[i])
#
#                 self.updateStatusBar('Selected Heading : ' + str(self.selected_column))
#                 break
#
#             i += 1
#         pass


 # self.UpdateAllListBoxesWithNewValues()

        # i = 0
        # for v in self.DATA_GRID_COL_HEADINGS:
        #     if v == self.values.get('_COMBO_COLUMNNAME_'):
        #         rename = self.values.get('_INPUT_COLUMN_RENAME_')
        #         data_type = self.values.get('_COMBO_DATATYPE_')
        #         action_to_perform = self.values.get('_COMBO_ACTION_')
        #
        #         self.COLUMN_RENAME_LIST[i] = rename  # connects to ListBox: _COLUMN_RENAME_HEADINGS_
        #         self.COLUMN_DATATYPE_LIST[i] = data_type  # connects to ListBox: _COLUMN_DATATYPE_
        #         self.COLUMN_ACTION_LIST[i] = action_to_perform  # connects to ListBox: _COLUMN_ACTION_
        #
        #         self.window.FindElement('_COLUMN_RENAME_HEADINGS_').Update(values=self.COLUMN_RENAME_LIST)
        #
        #         self.window.FindElement('_COLUMN_DATATYPE_').Update(values=self.COLUMN_DATATYPE_LIST)
        #
        #         self.window.FindElement('_COLUMN_ACTION_').Update(values=self.COLUMN_ACTION_LIST)
        #
        #         self.window.FindElement('_COMBO_COLUMNNAME_').Update(values=self.DATA_GRID_COL_HEADINGS)
        #
        #         break
        #     i += 1
        #
        # pass

# def UpdateAllListBoxesWithNewValues(self):
    #
    #     i = 0
    #     for v in self.DATA_GRID_COL_HEADINGS:
    #         if v == self.values.get('_COMBO_COLUMNNAME_'):
    #
    #             self.selected_column_by_integer = i
    #
    #             rename = self.values.get('_INPUT_COLUMN_RENAME_')
    #             data_type = self.values.get('_COMBO_DATATYPE_')
    #             action_to_perform = self.values.get('_COMBO_ACTION_')
    #
    #             self.COLUMN_RENAME_LIST[i] = rename  # connects to ListBox: _COLUMN_RENAME_HEADINGS_
    #             self.COLUMN_DATATYPE_LIST[i] = data_type  # connects to ListBox: _COLUMN_DATATYPE_
    #             self.COLUMN_ACTION_LIST[i] = action_to_perform  # connects to ListBox: _COLUMN_ACTION_
    #
    #             self.window.FindElement('_COLUMN_RENAME_HEADINGS_').Update(values=self.COLUMN_RENAME_LIST)
    #
    #             self.window.FindElement('_COLUMN_DATATYPE_').Update(values=self.COLUMN_DATATYPE_LIST)
    #
    #             self.window.FindElement('_COLUMN_ACTION_').Update(values=self.COLUMN_ACTION_LIST)
    #
    #             self.window.FindElement('_COMBO_COLUMNNAME_').Update(values=self.DATA_GRID_COL_HEADINGS)
    #
    #             break
    #         i += 1