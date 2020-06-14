"""
This class is designed to display data that has been obtained

    Data Types expected are:
    Headings -> []
    Data -> ?

"""
import PySimpleGUI as sg

class DataTablePopUp:

    # fh = DataTablePopUp(data_table_headings, data_table_data)
    def __init__(self, data_table_headings, data_table_data):
        self.data_table_headings = data_table_headings

        # Unsure what data type this is yet. JSON or [] or {} .. perhaps need to test and deal with appropriatley .
        # how does print deal with all the different data types?
        self.data_table_data = data_table_data

        self.containment()


    def anotherDefinition(self):


        pass

    def obtainScreenDetails(self):
        # These tweo will be closley linked
        import ScreenDetails as sd
        self.screen_details = sd.ScreenDetails().monitor_dictionary


    def containment(self):

        form_width = 120
        # ------ Make the Table Data ------
        DATA_GRID_COL_HEADINGS = ('','')
        DATA_GRID_MAX_ROWS = 0
        DATA_GRID_MAX_COLS = len(DATA_GRID_COL_HEADINGS)
        data = [[j for j in range(DATA_GRID_MAX_COLS)] for i in range(DATA_GRID_MAX_ROWS)]
        headings = list(DATA_GRID_COL_HEADINGS) # [str(data[0][x]) for x in range(len(data[0]))]

        def updateStatusBar(window, message):
            window.FindElement( '_STATUSBAR_').Update(message + '\n', append=True, autoscroll=True)

        def updateEventDisplayBar(window, message):
            window.FindElement('_EVENTDISPLAYBAR_').Update(message, append=False, autoscroll=False)


        table = sg.Table(
                values=self.data_table_data ,
                headings=self.data_table_headings,
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


        # Colour options: https://user-images.githubusercontent.com/46163555/71361827-2a01b880-2562-11ea-9af8-2c264c02c3e8.jpg
        sg.ChangeLookAndFeel('Dark Blue 3')

        # ------ Menu Definition ------ #
        # The only definition we need is.. Exit.
        menu_def = [['&File', [ 'E&xit', 'Properties']],
                    # ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
                    ['&Help', '&About...'], ]



        layout = [
            [sg.Menu(menu_def, tearoff=False)]   ,
            [
                sg.Text('1. TESTING CODE ONY ----------')
            ],
            [sg.Text('_' * form_width)],

            # Potential for input box:
                # How many records to display
                # Average density of records to display?

            [sg.Submit(key='_SUBMIT_', tooltip=''), sg.Cancel()],

            # to update: https://github.com/PySimpleGUI/PySimpleGUI/issues/1307
            # this will be a pop up  window
            [table]

        ]


        # https://github.com/PySimpleGUI/PySimpleGUI/issues/850
        window = sg.Window('DataTable:').Layout(layout)


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

            # if event == '_FILEBROWSE_':
                # TODO: Test that an acutal File was provided

                # file_name_and_path = values.get('_FILEBROWSE_')
                #
                #
                # if len(file_name_and_path) > 0:
                #     window.FindElement('_FILETOPROCESS_').Update(text_color='black')
                #     window.FindElement('_FILETOPROCESS_').Update(file_name_and_path)
                #
                #     h = fileHandler(file_name_and_path)
                #
                #     DATA_GRID_COL_HEADINGS = (h.column_headings)
                #
                #     window.FindElement('_COLUMNHEADINGS_').Update(values=DATA_GRID_COL_HEADINGS)
                #     window.FindElement('_COLUMNHEADINGS_').set_size((30, len(DATA_GRID_COL_HEADINGS)))
                #
                #     updateStatusBar(window, 'Column Headings : ' + ', '.join(DATA_GRID_COL_HEADINGS))
                #
                #
                #     DATA_GRID_MAX_COLS = len(h.column_headings)
                #     DATA_GRID_MAX_ROWS = len(h.data_list)
                #
                #     print(DATA_GRID_MAX_ROWS)
                #     print(DATA_GRID_MAX_COLS, ':', DATA_GRID_COL_HEADINGS)
                #
                #     print(h.data_list)
                #
                #     data = [
                #         [j for j in range(DATA_GRID_MAX_COLS)]
                #         for i in range(DATA_GRID_MAX_ROWS)
                #     ]
                #     headings = list(DATA_GRID_COL_HEADINGS)  # [str(data[0][x]) for x in range(len(data[0]))]
                #
                #     data = list(h.data_list)
                #     list = []
                #     for n in h.data_list:
                #     for key, value in h.data_list:
                #         temp = [key, value]
                #         print(temp)
                #         list.append(temp)
                #
                #     headings = list(h.column_headings)

            # but probably even better is this! -> https://github.com/PySimpleGUI/PySimpleGUI/issues/845


                    # and
        # https://www.reddit.com/r/PySimpleGUI/comments/erlssi/multiple_window_change_active_loop/
        #             for window in self.open_windows:
        #                 closed = window.run()
        #                 if closed:
        #                     self.open_windows.remove(window)

                    # window.FindElement('_DATATABLE_').Update(visible=True)
                    # window.FindElement('_DATATABLE_').Update(values = data)
                    # window.FindElement('_DATATABLE_').Update(headings=headings)

                    # window.FindElement('_DATAGRID_').set_size((800, 110))

                # else:
                #     window.FindElement('_FILETOPROCESS_').Update(text_color='gray')
                #     window.FindElement('_FILETOPROCESS_').Update('please select a file to process')


            # elif event == '_SUBMIT_' :
            #     updateStatusBar(window, 'STUB: With the file name in mind, process each line...')
            #     # l = Locality(window, file_name_and_path, "ClientAddress")
            #
            #     # print(l.data_list)
            #     # print(l.time_to_execute_seconds)
            #
            #     updateStatusBar(window, 'Completed processing : ' + str(l.time_to_execute_seconds))


                # 1. Need our list of headings. they are used for the array to be created.


        window.Close()





# This is just for testing this clas.
import random

data_table_headings = ['a','b', 'c']
num_cols = len(data_table_headings) + 1
num_rows = 5


def number(max_val=10):
    return random.randint(0, max_val)

def make_table(num_rows, num_cols):

    data =  [[j for j in range(num_cols)]for i in range(num_rows) ]

    for i in range(1, num_rows):
        data[i] = [ *[number() for i in range(num_cols - 1)]]

    return data


data_table_data = make_table(num_rows=num_rows, num_cols=num_cols)

dp = DataTablePopUp(data_table_headings,data_table_data)