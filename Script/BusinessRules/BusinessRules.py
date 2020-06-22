
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
        print(execution_dict["column_action_list"])


        # for column_name in execution_dict["column_headings"]:
        #     print(column_name)

        for col_headings, action_list in zip(execution_dict["column_headings"], execution_dict["column_action_list"]):
            # print(details["column_action_list"])
            print(f'col heading: {col_headings}')
            ...
            print(f'action list: {action_list}')

            if action_list == 'Full Address -> [Suburb],[State],[Postcode]':
                print("execute Address clean over this column")

                # Note in this version, Im passing in the entire data as a nested list array. In the future, only pass in the individual column?
                l = Locality(window, execution_dict["column_headings"], execution_dict["data_table_nested_list"], col_headings)
                return_data = l.data_nested_list
                # I think I should do this.
                execution_dict["data_table_nested_list"] = l.data_nested_list

                # print(return_data)

                # for rd in return_data:
                #     print(rd)




        #

        # all code below here was for a different branch.
        #   l = Locality(window, self.DATA_GRID_COL_HEADINGS, self.DATA_GRID_NESTED_LIST, self.selected_column)
        #   DATA_GRID_NESTED_LIST = l.data_nested_list

