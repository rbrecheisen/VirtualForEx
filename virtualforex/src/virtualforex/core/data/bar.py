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
    
    def range(self):
        return abs(self.high() - self.low())
    
    def body_range(self):
        return abs(self.open() - self.close())
    
    def __eq__(self, other):
        if not isinstance(other, Bar):
            return NotImplemented
        return other.open() == self.open() and other.high() == self.high() and other.low() == self.low() and other.close() == self.close()
    
    def __str__(self):
        return f'Bar(timestsamp={self.timestamp()}, open={self.open()}, high={self.high()}, low={self.low()}, close={self.close()})'