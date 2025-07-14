import datetime
import pandas as pd

from virtualforex.core.bar import Bar

class PriceData:
    DEFAULT_PAGE_SIZE = 100

    def __init__(self, data, name):
        self._data = data
        self._name = name
        self._first_idx = 0
        self._last_idx = 0
        self._last_bar = None
        self._page_size = PriceData.DEFAULT_PAGE_SIZE

    # GET/SET

    def name(self):
        return self._name
    
    def data(self):
        return self._data
    
    def last_bar(self):
        return self._last_bar
    
    def set_last_bar(self, last_bar):
        self._last_bar = last_bar
    
    def page_size(self):
        return self._page_size
    
    def set_page_size(self, page_size):
        self._page_size = page_size
    
    # UTILITY

    def start_date(self):
        return self.data().index[0]
    
    def end_date(self):
        return self.data().index[-1]
    
    def create_bar_from_row(self, row):
        return Bar(row['Open'], row['High'], row['Low'], row['Close'])
    
    def first_n(self, n):
        self._first_idx, self._last_idx = 0, n
        data = self.data().iloc[self._first_idx:self._last_idx]
        self.set_last_bar(self.create_bar_from_row(data.iloc[-1]))
        return data
    
    def last_n(self, n):
        self._first_idx, self._last_idx = len(self.data()) + 1 - n, len(self.data()) + 1
        data = self.data().iloc[self._first_idx:self._last_idx]
        self.set_last_bar(self.create_bar_from_row(data.iloc[-1]))
        return data
    
    def prev(self):
        if self._first_idx > 0:
            self._first_idx -= 1
            self._last_idx -= 1
        data = self.data().iloc[self._first_idx:self._last_idx]
        self.set_last_bar(self.create_bar_from_row(data.iloc[-1]))
        return data
    
    def prev_page(self):
        page_size = self.page_size()
        if self._first_idx > page_size:
            self._first_idx -= page_size
            self._last_idx -= page_size
        elif self._first_idx <= page_size:
            self._first_idx = 0
            self._last_idx = page_size
        data = self.data().iloc[self._first_idx:self._last_idx]
        self.set_last_bar(self.create_bar_from_row(data.iloc[-1]))
        return data

    def next(self):
        if self._last_idx < len(self.data()) + 1:
            self._first_idx += 1
            self._last_idx += 1
        data = self.data().iloc[self._first_idx:self._last_idx]
        self.set_last_bar(self.create_bar_from_row(data.iloc[-1]))
        return data
    
    def next_page(self):
        page_size = self.page_size()
        if self._last_idx < len(self.data()) + 1 - page_size:
            self._first_idx += page_size
            self._last_idx += page_size
        elif self._last_idx >= len(self.data()) + 1 - page_size:
            self._last_id = len(self.data()) + 1
            self._first_idx -= self._last_id - page_size
        data = self.data().iloc[self._first_idx:self._last_idx]
        self.set_last_bar(self.create_bar_from_row(data.iloc[-1]))
        return data
    
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
        data = self.data().iloc[self._first_idx:self._last_idx]
        self.set_last_bar(self.create_bar_from_row(data.iloc[-1]))
        return data
    
    def all(self):
        self._first_idx, self._last_idx = 0, len(self.data()) + 1
        data = self.data().iloc[self._first_idx:self._last_idx]
        self.set_last_bar(self.create_bar_from_row(data.iloc[-1]))
        return data