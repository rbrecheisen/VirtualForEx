from pandas import DataFrame as BaseDataFrame


class DataFrame(BaseDataFrame):
    def __init__(self):
        super(DataFrame, self).__init__()
        self._name = None

    def name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name