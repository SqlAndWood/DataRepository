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

        # The two combo boxes are populated from this information
        self.combo_datatype_list = list(('Text','Date', 'DateTime', 'Time', 'Integer','Decimal', 'Boolean'))
        self.combo_datatype_keys = self.combo_datatype_list

        self.combo_action_list = list(('Take no action', 'Full Address -> [Suburb],[State],[Postcode]','Date', 'Age'))
        self.combo_action_keys = list(('_A1_', '_A2_', '_A3_', ))


        self.form_width = 120