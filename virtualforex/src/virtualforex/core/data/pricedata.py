class PriceData:
    def __init__(self, df, symbol, timeframe):
        self._df = df
        self._symbol = symbol
        self._timeframe = timeframe

    def df(self):
        return self._df
    
    def symbol(self):
        return self._symbol
    
    def timeframe(self):
        return self._timeframe
    
    def start_date(self):
        return self.df().index[0]

    def end_date(self):
        return self.df().index[-1]