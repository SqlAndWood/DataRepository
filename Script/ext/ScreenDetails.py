class ScreenDetails:


    def __init__(self):
        self.monitor_dictionary = self.main()


    def main(self):

        from screeninfo import get_monitors

        monitor_dict = []

        for m in get_monitors():
            monitor_dict.append( {
                                    "name" : m.__getattribute__('name').replace("\\", "").replace(".", ""),
                                    "height_mm" : m.__getattribute__('height_mm'),
                                    "width_mm" : m.__getattribute__('width_mm'),
                                    "height(" : m.__getattribute__('height'),
                                    "width" : m.__getattribute__('width'),
                                    "x" : m.__getattribute__('x'),
                                    "y" : m.__getattribute__('y'),
                                    "monitor_count": len(get_monitors())
                                    })

        return monitor_dict
