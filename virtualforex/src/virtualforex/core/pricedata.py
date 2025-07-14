import datetime
import pandas as pd


class PriceData:
    def __init__(self, data, name):
        self._data = data
        self._name = name
        self._first_idx = 0
        self._last_idx = 0
        self._page_size = 50

    # GET/SET

    def name(self):
        return self._name
    
    def data(self):
        return self._data
    
    def page_size(self):
        return self._page_size
    
    def set_page_size(self, page_size):
        self._page_size = page_size
    
    # UTILITY

    def start_date(self):
        return self.data().index[0]
    
    def end_date(self):
        return self.data().index[-1]
    
    def first_n(self, n):
        self._first_idx, self._last_idx = 0, n
        return self.data().iloc[self._first_idx:self._last_idx]
    
    def last_n(self, n):
        self._first_idx, self._last_idx = len(self.data()) + 1 - n, len(self.data()) + 1
        return self.data().iloc[self._first_idx:self._last_idx]
    
    def prev(self):
        if self._first_idx > 0:
            self._first_idx -= 1
            self._last_idx -= 1
        # print(f'PriceData.prev() range = {self._last_idx - self._first_idx} candles')
        return self.data().iloc[self._first_idx:self._last_idx]
    
    def prev_page(self):
        page_size = self.page_size()
        if self._first_idx > page_size:
            self._first_idx -= page_size
            self._last_idx -= page_size
        elif self._first_idx <= page_size:
            self._first_idx = 0
            self._last_idx = page_size
        # print(f'PriceData.prev_page() range = {self._last_idx - self._first_idx} candles')
        return self.data().iloc[self._first_idx:self._last_idx]

    def next(self):
        if self._last_idx < len(self.data()) + 1:
            self._first_idx += 1
            self._last_idx += 1
        # print(f'PriceData.next() range = {self._last_idx - self._first_idx} candles')
        return self.data().iloc[self._first_idx:self._last_idx]
    
    def next_page(self):
        page_size = self.page_size()
        if self._last_idx < len(self.data()) + 1 - page_size:
            self._first_idx += page_size
            self._last_idx += page_size
        elif self._last_idx >= len(self.data()) + 1 - page_size:
            self._last_id = len(self.data()) + 1
            self._first_idx -= self._last_id - page_size
        # print(f'PriceData.next_page() range = {self._last_idx - self._first_idx} candles')
        return self.data().iloc[self._first_idx:self._last_idx]
    
    def jump_to_date(self, new_date):
        page_size = self.page_size()
        if isinstance(new_date, pd.Timestamp):
            date = new_date
        elif isinstance(new_date, (datetime.date, datetime.datetime)):
            date = pd.Timestamp(new_date)
        else:
            date = pd.Timestamp(new_date.toPython())
        self._first_idx = self.data().index.get_indexer([date], method='nearest')[0]
        self._last_idx = self._first_idx + page_size
        if self._last_idx > len(self.data()) + 1:
            self._last_idx = len(self.data()) + 1
        return self.data().iloc[self._first_idx:self._last_idx]
    
    def all(self):
        self._first_idx, self._last_idx = 0, len(self.data()) + 1
        return self.data().iloc[self._first_idx:self._last_idx]
