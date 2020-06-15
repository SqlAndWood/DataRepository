class DataConverter:

    # fh = DataConverter(data_to_convert)
    def __init__(self, data_to_convert):

        self.data_to_convert = data_to_convert

        self.data_nested_list = self.createNestedList()


    # https://snakify.org/en/lessons/two_dimensional_lists_arrays/
    def createNestedList(self):

        # if isinstance(self.data_list , list):
        #     print('list of..')

        record = []

        for n in self.data_to_convert:
            # if isinstance(n, dict):
            #     print('dict of ...')
            # https://www.ict.social/python/basics/multidimensional-lists-in-python
            column = []
            for value in list(n.values()):
                column.append(value)

            record.append(column)

        return record

    def printNestedList(self, nested_list):
        for column in nested_list:
            for item in column:
                print(item, end=" ")

    # return a column from within an multimensional array.
    # https://stackoverflow.com/questions/903853/how-do-you-extract-a-column-from-a-multi-dimensional-array
    def column(self, nested_list, column_number):
        return [row[column_number] for row in nested_list]