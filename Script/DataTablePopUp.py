"""
This class is designed to display data that has been obtained

    Data Types expected are:
    Headings -> []
    Data -> [ [] , [], [] ]

"""
import PySimpleGUI as sg

class DataTablePopUp:

    # fh = DataTablePopUp(data_table_headings, data_table_data)
    def __init__(self, data_table_headings, data_table_data, data_description):

        self.form_width = 120
        self.debug_font = ("courier", 10)

        self.data_description = data_description
        self.data_table_headings = data_table_headings

        self.data_table_data = data_table_data

        self.containment()


    def obtainScreenDetails(self):
        # These tweo will be closley linked
        import ScreenDetails as sd
        self.screen_details = sd.ScreenDetails().monitor_dictionary


    def containment(self):

        # https://github.com/PySimpleGUI/PySimpleGUI/blob/master/PySimpleGUI.py
        table = sg.Table(
                values=self.data_table_data ,
                headings=self.data_table_headings,
                max_col_width=25,
                background_color='lightblue',
                auto_size_columns=False,
                display_row_numbers=True,
                justification='left',
                num_rows=min(len(self.data_table_data), 30) ,
                alternating_row_color='gray',
                vertical_scroll_only=False,
                hide_vertical_scroll=False,
                font = self.debug_font,
                key='_DATATABLE_'
                # tooltip='This is a table'
            )

        sg.ChangeLookAndFeel('Dark Blue 3')

        # ------ Menu Definition ------ #
        menu_def = [['&File', [ 'E&xit', 'Properties']],
                    ['&Help', '&About...'], ]

        layout = [
            [sg.Menu(menu_def, tearoff=False)],

            # to update: https://github.com/PySimpleGUI/PySimpleGUI/issues/1307
            [table],
            [sg.Text('_' * self.form_width)]

        ]

        # https://github.com/PySimpleGUI/PySimpleGUI/issues/850
        window = sg.Window('Data Source: ' + self.data_description ).Layout(layout)

        #https://stackoverflow.com/questions/55515627/pysimplegui-call-a-function-when-pressing-button
        # While Loop might not be necessary.
        while True:

            event, values = window.Read()

            if event is not None:
                print(event, values)
                pass

            # This makes the app stop when you press X (close)
            elif event is None:
                break


        window.Close()


# This is just for testing this class
# from fileHandler import *
# h = fileHandler("I:\git\WordToExcel\Data\\20200602\\20200609 RIF ClientDetails.csv")
# dp = DataTablePopUp(data_table_headings = h.column_headings,data_table_data = h.data_nested_list, data_description = h.file_name)