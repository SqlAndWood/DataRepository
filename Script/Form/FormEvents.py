import time

from Form import GenericPopUp as gpu
from DataTablePopUp import *
from ext import fileHandler as fh

# Great example of filtering on a list() : https://github.com/PySimpleGUI/PySimpleGUI/issues/1633
# new_values = [x for x in names if search in x]

class FormEvents:

    # fh = FormEvents()
    def __init__(self,  layout, app_config):
        # DO NOT SET WINDOW to self.window! for some reason this really slows down the GUI responsiveness.
        window = sg.Window('Data Cleansing', layout, finalize=True)
        self.app_config = app_config

        self.file_name_and_path = ""
        self.selected_column_by_integer = 0
        self.selected_column = ""

        # self.DATA_GRID_NESTED_LIST = []  # Represents the full Data pulled back from the 'file'
        self.DATA_GRID_COL_HEADINGS = []  # connects to ListBox: _COLUMN_HEADINGS_
        self.COLUMN_RENAME_LIST = []  # connects to ListBox: _COLUMN_RENAME_HEADINGS_
        self.COLUMN_DATATYPE_LIST = []  # connects to ListBox: _COLUMN_DATATYPE_
        self.COLUMN_ACTION_LIST = []  # connects to ListBox: _COLUMN_ACTION_

        self.FormExecution(window)


    def OpenFileAndDisplay(self,window, values):

        self.file_name_and_path = values.get('_FILEBROWSE_')

        if len(self.file_name_and_path) > 0:
            self.file_containing_data = fh.fileHandler(self.file_name_and_path)
            self.DATA_GRID_COL_HEADINGS = self.file_containing_data.column_headings
            self.DATA_GRID_NESTED_LIST = self.file_containing_data.data_nested_list

            window['_FILETOPROCESS_'](text_color='black') # short hand for updating an element.
            window['_FILETOPROCESS_'](self.file_name_and_path)# short hand for updating an element.

            self.COLUMN_RENAME_LIST = self.DATA_GRID_COL_HEADINGS.copy()  # connects to ListBox: _COLUMN_RENAME_HEADINGS_
            self.COLUMN_DATATYPE_LIST = [''] * len(self.DATA_GRID_COL_HEADINGS)  # connects to ListBox: _COLUMN_DATATYPE_
            self.COLUMN_ACTION_LIST = [''] * len(self.DATA_GRID_COL_HEADINGS)  # connects to ListBox: _COLUMN_ACTION_

            # Load the Combo box with array of values.
            window.FindElement('_COMBO_COLUMNNAME_').Update(values=self.DATA_GRID_COL_HEADINGS) #Long hand way to update an element.

            # this is an ambiguous function name; however I am returning the current list information to the Form fo rthe user to know what they have selected.
            self.UpdateListBoxes(window)
            self.UpdateUserInputs(window)
            self.HighlightAssociatedListBox(window)

        else:
            window.FindElement('_FILETOPROCESS_').Update(text_color='gray')
            window.FindElement('_FILETOPROCESS_').Update('please select a file to process')


    def IdentifyIndexSelected(self, values, key):
        # https://www.programiz.com/python-programming/methods/list/index  -> index = vowels.index('e')

        if isinstance(values.get( key), str):
            self.selected_column = values.get(key)
            self.selected_column_by_integer = self.DATA_GRID_COL_HEADINGS.index(values.get(key))

        elif isinstance(values.get(key), list):
            self.selected_column = values.get(key)[0]
            self.selected_column_by_integer = 0
            if self.selected_column != "":
                try:
                    self.selected_column_by_integer = self.DATA_GRID_COL_HEADINGS.index(self.selected_column)
                except ValueError:
                    pass


    def HighlightAssociatedListBox(self,window):
        window.FindElement('_COLUMN_HEADINGS_').Update(set_to_index=self.selected_column_by_integer)
        window.FindElement('_COLUMN_RENAME_HEADINGS_').Update(set_to_index=self.selected_column_by_integer)
        window.FindElement('_COLUMN_DATATYPE_').Update(set_to_index=self.selected_column_by_integer)
        window.FindElement('_COLUMN_ACTION_').Update(set_to_index=self.selected_column_by_integer)


    def UpdateUserInputs(self,window):  #These are the three single line Inputs
        window.FindElement('_COMBO_COLUMNNAME_').Update(value=self.DATA_GRID_COL_HEADINGS[self.selected_column_by_integer])
        window.FindElement('_INPUT_COLUMN_RENAME_').Update(value=self.COLUMN_RENAME_LIST[self.selected_column_by_integer])
        window.FindElement('_COMBO_DATATYPE_').Update(value=self.COLUMN_DATATYPE_LIST[self.selected_column_by_integer])
        window.FindElement('_COMBO_ACTION_').Update(value=self.COLUMN_ACTION_LIST[self.selected_column_by_integer])


    def UpdateListBoxes(self,window):
        window.FindElement('_COLUMN_HEADINGS_').Update(values=self.DATA_GRID_COL_HEADINGS)
        window.FindElement('_COLUMN_HEADINGS_').set_size((30, len(self.DATA_GRID_COL_HEADINGS)))  # ie, configure Height to the number of Column Headers

        window.FindElement('_COLUMN_RENAME_HEADINGS_').Update(values=self.COLUMN_RENAME_LIST)
        window.FindElement('_COLUMN_RENAME_HEADINGS_').set_size((30, len(self.COLUMN_RENAME_LIST)))  # ie, configure Height to the number of Column Headers

        window.FindElement('_COLUMN_DATATYPE_').Update(values=self.COLUMN_DATATYPE_LIST)
        window.FindElement('_COLUMN_DATATYPE_').set_size((30, len(self.COLUMN_DATATYPE_LIST)))  # ie, configure Height to the number of Column Headers

        window.FindElement('_COLUMN_ACTION_').Update(values=self.COLUMN_ACTION_LIST)
        window.FindElement('_COLUMN_ACTION_').set_size((30, len(self.COLUMN_ACTION_LIST)))  # ie, configure Height to the number of Column Headers


    def UpdateAllThreeLists_KeyPressChangeEvent(self,values):
        self.COLUMN_RENAME_LIST[self.selected_column_by_integer] = values.get('_INPUT_COLUMN_RENAME_')  # connects to ListBox: _COLUMN_RENAME_HEADINGS_
        self.COLUMN_DATATYPE_LIST[self.selected_column_by_integer] = values.get('_COMBO_DATATYPE_')  # connects to ListBox: _COLUMN_DATATYPE_
        self.COLUMN_ACTION_LIST[self.selected_column_by_integer] =  values.get('_COMBO_ACTION_')  # connects to ListBox: _COLUMN_ACTION_


    def ViewDataViaPopUpWindow(self):
        if self.file_name_and_path != "":
            DataTablePopUp(data_table_headings=self.DATA_GRID_COL_HEADINGS, data_table_data=self.DATA_GRID_NESTED_LIST,
                           data_description=self.file_containing_data.file_name)
        else:

            gpu.GenericPopUp (
                                self.app_config,
                                window_title = "No Data to View",
                                statement = 'Please select a file prior to viewing associated data.'
                             )

    # TODO: Save Data to a location of the persons choosing with the file of their choosing.
    def SaveData(self):
        if self.file_name_and_path != "":
            self.file_containing_data.SaveTempFile("temp.csv", self.COLUMN_RENAME_LIST, self.DATA_GRID_NESTED_LIST)
        else:
            gpu.GenericPopUp(
                self.app_config,
                window_title="No Data to Save",
                statement='Please select a file prior to saving associated data.'
            )


    def FormExecution(self, window):

        while True:

            event, values = window.Read()

            # Allow the app to quit when you press X (close)
            if event in (sg.WIN_CLOSED, 'Exit', None):
                # self.updateStatusBar(window, event, values)
                break

            # Action #1: Without a File browse, nothing else will occur.
            if event == '_FILEBROWSE_':
                self.OpenFileAndDisplay(window, values)

            # Action #2: A 'Column' must first be selected from the command button.
                # upon the user selecting from the command button, associated List Box Pos will be Highlighted.
            elif event == '_COMBO_COLUMNNAME_':  # Update associated collumn on click.
                self.IdentifyIndexSelected(values, '_COMBO_COLUMNNAME_')
                # this is an ambiguous function name; however I am returning the current list information to the Form fo rthe user to know what they have selected.
                self.UpdateUserInputs(window)
                self.HighlightAssociatedListBox(window)


            # Alternative Action #2, a User might accidently select from teh List Box itself. if they do, ...
            elif event == '_COLUMN_HEADINGS_':  # Update associated collumn on click.
                self.IdentifyIndexSelected(values,event)
                # this is an ambiguous function name; however I am returning the current list information to the Form fo rthe user to know what they have selected.
                self.UpdateUserInputs(window)
                self.HighlightAssociatedListBox(window)


            # Alternaive Action #2; If one of these boxes are selected, ignore the selection, reset values back to previous selection.
            elif event in ( '_COLUMN_RENAME_HEADINGS_' ,'_COLUMN_DATATYPE_','_COLUMN_ACTION_'):

                # this is an ambiguous function name; however I am returning the current list information to the Form fo rthe user to know what they have selected.
                self.UpdateUserInputs(window)
                self.HighlightAssociatedListBox(window)


            # Action #3: The following three controls are updated with the same code.
               # Update the List Boxes with the provided details.
            elif event in ( '_INPUT_COLUMN_RENAME_' ,'_COMBO_DATATYPE_' ,'_COMBO_ACTION_') :
                # start_time = time.time()
                self.UpdateAllThreeLists_KeyPressChangeEvent(values)
                self.UpdateListBoxes(window)

                # this is an ambiguous function name; however I am returning the current list information to the Form fo rthe user to know what they have selected.
                self.UpdateUserInputs(window)
                self.HighlightAssociatedListBox(window)
                # print("---Three over arching things chagned:  %s seconds ---" % (time.time() - start_time))


            # The very last step in the entire process. This is the Action shot.
            elif event == '_EXECUTE_':
                from BusinessRules import BusinessRules as br
                f = br.BusinessRules(window,  values)


            # at any time you may save the data you have compiled.
            elif event == '_SAVEDATA_':
                self.SaveData()

            # at any time, you may view the data you have compiled.
            elif event == '_VIEWDATA_':
                self.ViewDataViaPopUpWindow()


        window.Close()