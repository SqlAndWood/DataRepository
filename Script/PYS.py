# https://pysimplegui.readthedocs.io/en/latest/
import PySimpleGUI as sg

# Colour options: https://user-images.githubusercontent.com/46163555/71361827-2a01b880-2562-11ea-9af8-2c264c02c3e8.jpg
sg.ChangeLookAndFeel('Dark Blue 3')


# Open a file using a file menu thingo.

# Creat the layout based on the file selected.

# Based on the user inputs, perform surgery on the data.

# ------ Menu Definition ------ #
menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
            ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Help', '&About...'], ]

# ------ Column Definition ------ #


lb_column_headings = ('First Name', 'Surname', 'Full Address','DOB', 'Phone Number')
lb_action_to_apply = ('Full Address -> [Suburb],[State],[Postcode]','')

form_width = 120

layout = [
    [sg.Menu(menu_def, tearoff=False)]   ,
    [
        sg.Text('1. Select the file to process.\n2. Select the column to deidentify. \n3. Select the method to deidentify.'
             '\n4. Select the output file location.')
    ],
    [sg.Text('_' * form_width)],

    # sg.InputText('', size=(60, 1), justification='left'),
    # https://github.com/PySimpleGUI/PySimpleGUI/issues/850
    [sg.Text('1. Select File:', size=(10, 1), auto_size_text=False, justification='left')],
    [sg.Input(key='_FILEBROWSE_', enable_events=True, visible=False)],
    [
    sg.FileBrowse (
                    button_text="Browse",
                    file_types=( ('CSV Files', '*.csv'),('TXT Files', '*.txt'),('All Files', '*.*')),
                    initial_folder=None,
                    target='_FILEBROWSE_'
                    )
    ],

    [sg.Text('_' * form_width)],
    [
        sg.Frame('Column Headings',[[sg.Listbox(values=lb_column_headings, size=(30, len(lb_column_headings)))]], title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='Oh Boy!')
        ,
        sg.Frame('Action to Apply',[[sg.Listbox(values=lb_action_to_apply, size=(form_width-40, len(lb_action_to_apply)))]], title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='Oh Boy!')
    ],
    [sg.Text('_' * form_width)],
    [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]
]



# https://github.com/PySimpleGUI/PySimpleGUI/issues/850
# window = sg.Window('A whole new world!', layout, default_element_size=(40, 1), grab_anywhere=False)
window = sg.Window('A whole new world!').Layout(layout)

while True:             # Event Loop
    event, values = window.Read()
    if event is None:
        break
    print(event, values)
# event, values = window.read()
# window.close()

sg.Popup('Title',
         'The results of the window.',
         'The button clicked was "{}"'.format(event),
         'The values are', values)