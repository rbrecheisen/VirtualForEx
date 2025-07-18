from virtualforex.core.data.bar import Bar


class PriceDataWindow:
    def __init__(self, price_data):
        self._price_data = price_data
        self._first_index = 0
        self._last_index = len(price_data.df())
        self._page_size = 100
        self._last_bar = None

    # GET/SET

    def price_data(self):
        return self._price_data
    
    def df(self):
        return self._price_data.df()
    
    def page_size(self):
        return self._page_size
    
    def set_page_size(self, page_size):
        self._page_size = page_size
    
    def last_bar(self):
        if not self._last_bar:
            self._last_bar = self.create_bar_from_row(self.df().iloc[-1])
        return self._last_bar
    
    # HELPERS

    def create_bar_from_row(self, row):
        return Bar(row.name, row['Open'], row['High'], row['Low'], row['Close'])
    
    # SLICING

    def page(self, first_index, last_index):
        self._first_index, self._last_index = first_index, last_index
        df = self.df().iloc[self._first_index:self._last_index]
        self._last_bar = self.create_bar_from_row(df.iloc[-1])
        return df
    
    def current_page(self):
        return self.page(self._first_index, self._last_index)
    
    def random_page(self):
        import random
        nr_pages = len(self.df()) // self.page_size()
        random_page = random.randint(0, nr_pages - 1)
        self._first_index = random_page * self.page_size()
        self._last_index = self._first_index + self.page_size()
        return self.page(self._first_index, self._last_index)

    def first_page(self):
        return self.page(0, self.page_size())

    def last_page(self):
        return self.page(len(self.df()) - self.page_size(), len(self.df()))
    
    def next(self):
        if self._last_index < (len(self.df()) - 1):
            self._first_index += 1
            self._last_index += 1
        return self.page(self._first_index, self._last_index)
    
    def next_page(self):
        if self._last_index < (len(self.df()) - self.page_size()):
            self._first_index += self.page_size()
            self._last_index += self.page_size()
        elif self._last_index >= (len(self.df()) - self.page_size()):
            self._last_index = len(self.df())
            self._first_index = self._last_index - self.page_size()
        else:
            pass
        return self.page(self._first_index, self._last_index)
    
    def prev(self):
        if self._first_index > 0:
            self._first_index -= 1
            self._last_index -= 1
        return self.page(self._first_index, self._last_index)
    
    def prev_page(self):
        if self._first_index > self.page_size():
            self._first_index -= self.page_size()
            self._last_index -= self.page_size()
        elif self._first_index <= self.page_size():
            self._first_index = 0
            self._last_index = self.page_size()
        return self.page(self._first_index, self._last_index)
    
    def reset(self):
        self._first_index = 0
        self._last_index = len(self.df())
        return self.page(self._first_index, self._last_index)