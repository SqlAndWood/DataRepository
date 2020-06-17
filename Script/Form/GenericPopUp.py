import PySimpleGUI as sg

# fh = GenericPopUp()
class GenericPopUp:

    def __init__(self, app_config, window_title, statement):
        sg.ChangeLookAndFeel(app_config.look_and_feel)

        layout = [
                    [sg.Text(statement)],
                    [sg.Button('Ok'), sg.Button('Cancel')]
                 ]

        window = sg.Window(window_title, layout)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event in('Ok', 'Cancel'):
                break

        window.close()