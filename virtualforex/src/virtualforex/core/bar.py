class Bar:
    def __init__(self, timestamp, open, high, low, close):
        self._timestamp = timestamp
        self._open = open
        self._high = high
        self._low = low
        self._close = close

    def timestamp(self):
        return self._timestamp

    def open(self):
        return self._open
    
    def high(self):
        return self._high
    
    def low(self):
        return self._low
    
    def close(self):
        return self._close
    
    def __str__(self):
        return f'Bar(timestsamp={self.timestamp()}, open={self.open()}, high={self.high()}, low={self.low()}, close={self.close()})'