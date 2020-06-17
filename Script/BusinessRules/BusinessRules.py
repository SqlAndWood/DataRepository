
from DataClensing.Locality import Locality


class BusinessRules:
    """
       
    """

    # fh = FormEvents()
    def __init__(self,window, values ):

        self.file_name_and_path = values.get('_FILEBROWSE_')

        if self.file_name_and_path != "":

            if (self.selected_column == ""):
                print('Column heading not selected! ')  # do this first prior to continuing.

            self.updateStatusBar('STUB: With the file name in mind, process each line...')

            l = Locality(window, self.DATA_GRID_COL_HEADINGS, self.DATA_GRID_NESTED_LIST, self.selected_column)
            DATA_GRID_NESTED_LIST = l.data_nested_list

            self.updateStatusBar('Completed processing : ' + str(l.time_to_execute_seconds))

            window.FindElement('_COLUMN_HEADINGS_').Update(values=self.DATA_GRID_COL_HEADINGS)
            window.FindElement('_COLUMN_HEADINGS_').set_size((30, len(self.DATA_GRID_COL_HEADINGS)))

            # d = Dates(window, DATA_GRID_COL_HEADINGS, DATA_GRID_NESTED_LIST, self.selected_column)
            # We need a way to deal with a Data set, rather than always opening the file.