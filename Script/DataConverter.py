class DataConverter:

    # fh = DataConverter(data_to_convert)
    def __init__(self, data_to_convert):

        self.data_to_convert = data_to_convert

        self.data_nested_list = self.createNestedList()


    def createNestedList(self):

        # if isinstance(self.data_list , list):
        #     print('list of..')

        record = []

        for n in self.data_to_convert :
            # if isinstance(n, dict):
            #     print('dict of ...')
            # https://www.ict.social/python/basics/multidimensional-lists-in-python
            column = []
            for value in list(n.values()):
                column.append(value)

            record.append(column)

        return record

