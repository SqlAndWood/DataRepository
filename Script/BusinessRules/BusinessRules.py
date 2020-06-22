
from DataClensing.Locality import Locality


class BusinessRules:
    """
             execution_dict = {
                                'file_name_and_path':self.file_name_and_path,
                                'selected_column_by_integer':self.selected_column_by_integer ,
                                'selected_column':   self.selected_column ,
                                "column_headings": self.DATA_GRID_COL_HEADINGS,
                                "column_rename": self.COLUMN_RENAME_LIST,
                                "column_data_Type":  self.COLUMN_DATATYPE_LIST,
                                "column_action_list": self.COLUMN_ACTION_LIST,
                                "data_table_nested_list": self.DATA_GRID_NESTED_LIST
                                }

    """

    # fh = FormEvents()
    def __init__(self,window, values, execution_dict ):


        # loop each column in execution_dict["column_headings"]
        print(execution_dict["column_headings"])
        print(execution_dict["column_rename"])

        #

        # all code below here was for a different branch.
        #   l = Locality(window, self.DATA_GRID_COL_HEADINGS, self.DATA_GRID_NESTED_LIST, self.selected_column)
        #   DATA_GRID_NESTED_LIST = l.data_nested_list

