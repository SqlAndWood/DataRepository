import PySimpleGUI as sg


def define_gui_layout(app_config):
    """
        Starts and executes the GUI
        Reads data from a Queue and displays the data to the window
        Returns when the user exits / closes the window
        """
    # Colour options: https://user-images.githubusercontent.com/46163555/71361827-2a01b880-2562-11ea-9af8-2c264c02c3e8.jpg
    sg.ChangeLookAndFeel(app_config.look_and_feel)

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
                initial_folder=app_config.default_file_location,
                target='_FILEBROWSE_',
                size = command_button_size
            ),
            sg.Submit("View Data", key='_VIEWDATA_', tooltip='', size=command_button_size)
        ],
        [sg.Text('_' * app_config.form_width)],

        [
            sg.Frame('Column Headings',
                     [[sg.Listbox(key='_COLUMN_HEADINGS_', enable_events=True, values=app_config.column_heading_list,
                                  select_mode='single', size=(30, len(app_config.column_heading_list)))]],
                     title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='')
            ,
            sg.Frame('Rename Column',
                     [[sg.Listbox(key='_COLUMN_RENAME_HEADINGS_', enable_events=True, values=app_config.column_heading_list,
                                  size=(30, len(app_config.column_heading_list)))]],
                     title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='')
            ,
            sg.Frame('DataType Column',
                     [[sg.Listbox(key='_COLUMN_DATATYPE_', enable_events=True, values=app_config.column_heading_list,
                                  size=(30, len(app_config.column_heading_list)))]],
                     title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='')
            ,
            sg.Frame('Action to Apply on Column',
                     [[sg.Listbox(key='_COLUMN_ACTION_', enable_events=True, values=app_config.column_heading_list,
                                  size=(30, len(app_config.column_heading_list)))]],
                     title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='')
        ],

        [
            sg.Frame('Select Column',
                     [[sg.InputCombo(values='', enable_events=True, key='_COMBO_COLUMNNAME_', size=(30, 1))]],
                     title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='', size=(36, 1))
            ,
            sg.Frame('Rename Column',
                     [[sg.InputText(key='_INPUT_COLUMN_RENAME_', change_submits=True, size=(30, 1))]],
                     title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='', size=(36, 1))
            ,
            sg.Frame('Select DataType',
                     [[sg.InputCombo(values=app_config.combo_datatype_list, key='_COMBO_DATATYPE_', change_submits=True, size=(30, 1))]],
                     title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='', size=(36, 1))
            ,
            sg.Frame('Select Action',
                     [[sg.InputCombo(values=app_config.combo_action_list, key='_COMBO_ACTION_', change_submits=True, size=(30, 1))]],
                     title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='', size=(36, 1))
        ],
        # [
        #     sg.Submit("Update Definition", key='_UPDATE_COLUMN_DEFINITION_', tooltip='STUB', size=command_button_size)
        # ],
        [sg.Text('_' * app_config.form_width)],
        [
            sg.Submit("Process", key='_PROCESS_', tooltip='STUB', size=command_button_size),
            sg.Submit("UNDO ALL", key='_UNDO_', tooltip='STUB', size=command_button_size)
        ],
        [sg.Text('_' * app_config.form_width)],
        [
            sg.Submit(key='_SUBMIT_', tooltip='', size=command_button_size),
            sg.Cancel(size=command_button_size),
            sg.Submit("View Data", key='_VIEWDATA_', tooltip='', size=command_button_size),
            sg.Submit("Save Data", key='_SAVEDATA_', tooltip='', size=command_button_size)
        ],
        [sg.Multiline(key='_STATUSBAR_', size=(110, 5), auto_size_text=False, text_color='white',
                      background_color='lightslategray', visible=app_config.controls_visible_for_debug,
                      font=app_config.controls_debug_font)],
        [sg.Multiline(key='_EVENTDISPLAYBAR_', size=(110, 2), auto_size_text=False, text_color='white',
                      background_color='lightslategray', visible=app_config.controls_visible_for_debug,
                      font=app_config.controls_debug_font)],

    ]

    # https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Multithreaded_Long_Tasks.py
    return layout


if __name__ == '__main__':

    from applicationSettings import Configurations as config
    app_config = config.Configurations()

    layout = define_gui_layout(app_config)

    from Form import FormEvents as fe
    f = fe.FormEvents( layout)

    print('Exiting Program')