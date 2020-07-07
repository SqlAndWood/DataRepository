import os

from ext import ScreenDetails as sd


class Configurations:

    # fh = Configurations()
    def __init__(self):
        # There are four list boxes, initialise identically.
        # Each will need to be updated as the program advances.
        self.column_heading_list = ('',)
        self.column_heading_keys = ('',)

        self.rename_column_heading_list = self.column_heading_list
        self.rename_column_heading_keys = self.column_heading_keys

        self.colum_datatype_list = self.column_heading_list
        self.colum_datatype_keys = self.column_heading_keys

        self.action_list = self.column_heading_list
        self.action_keys = self.column_heading_keys

        self.combo_datatype_list = self.sortValues(
            ['Text', 'Date', 'DateTime', 'Time', 'Integer', 'Decimal', 'Boolean'])

        self.combo_datatype_keys = self.combo_datatype_list

        self.combo_action_list = list(('No action', 'Full Address -> [Suburb],[State],[Postcode]', 'Date', 'Age'))
        self.combo_action_keys = list(('_A1_', '_A2_', '_A3_',))

        # PySimpleGUI element sizes refer to (x, y) x = Character width, y = Number of characters tall
        self.form_width = 180

        self.look_and_feel = 'Dark Blue 3'
        self.controls_visible_for_debug = True
        self.controls_debug_font = ("courier", 10)

        self.screen_details = sd.ScreenDetails().monitor_dictionary

        # TODO: Relative Referencing required
        #         self.default_file_location = os.path.abspath(os.path.dirname("")).

    def sortValues(self, datatype):
        datatype.sort()
        # l = list(datatype)
        # print (l)
        return datatype
