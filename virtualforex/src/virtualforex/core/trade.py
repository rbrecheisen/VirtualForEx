class Trade:
    def __init__(self):
        self._symbol = None
        self._timeframe = None
        self._buy_stop = None
        self._sell_stop = None
        self._stop_loss = None
        self._take_profit = None
        self._active = False
        self._lot_size = 10000
        self._profit = 0.0
        self._bars = []

    def symbol(self):
        return self._symbol
    
    def set_symbol(self, symbol):
        self._symbol = symbol

    def timeframe(self):
        return self._timeframe
    
    def set_timeframe(self, timeframe):
        self._timeframe = timeframe

    def buy_stop(self):
        return self._buy_stop
    
    def set_buy_stop(self, buy_stop):
        if self.sell_stop():
            raise RuntimeError('Cannot set buy and sell stop simultaneously')
        self._buy_stop = buy_stop

    def sell_stop(self):
        return self._sell_stop
    
    def set_sell_stop(self, sell_stop):
        if self.buy_stop():
            raise RuntimeError('Cannot set buy and sell stop simultaneously')
        self._sell_stop = sell_stop

    def stop_loss(self):
        return self._stop_loss
    
    def set_stop_loss(self, stop_loss):
        self._stop_loss = stop_loss

    def take_profit(self):
        return self._take_profit
    
    def set_take_profit(self, take_profit):
        self._take_profit = take_profit

    def active(self):
        return self._active
    
    def profit(self):
        return self._profit
    
    def calculate_profit(self, exit_price, entry_price):
        self._profit = (exit_price - entry_price) * self._lot_size / exit_price

    def calculate_loss(self, exit_price, entry_price):
        self._profit = (entry_price - exit_price) * self._lot_size / entry_price

    def bars(self):
        return self._bars

    # HELPERS

    def add_bar(self, bar):
        self.bars().append(bar)

    def is_active(self):
        return self._active

    def buy_stop_hit(self, price):
        if self.buy_stop() and not self._active: # do not check hitting stop if trade already active
            hit = price > self.buy_stop()
            if hit:
                self._active = True
            return hit
        return False
    
    def sell_stop_hit(self, price):
        if self.sell_stop() and not self._active: # do not check hitting stop if trade already active
            hit = price < self.sell_stop()
            if hit:
                self._active = True
            return hit
        return False

    def stop_loss_hit(self, price):
        if self.buy_stop():
            hit = price < self.stop_loss()
            if hit:
                if self._active: # only calculate profit if trade was active
                    self.calculate_loss(exit_price=self.stop_loss(), entry_price=self.buy_stop())
                self._active = False
            return hit
        if self.sell_stop():
            hit = price > self.stop_loss()
            if hit:
                if self._active:
                    self.calculate_loss(exit_price=self.stop_loss(), entry_price=self.sell_stop())
                self._active = False
            return hit
        return False
    
    def take_profit_hit(self, price):
        if self.buy_stop():
            hit = price > self.take_profit()
            if hit:
                if self._active:
                    self.calculate_profit(exit_price=self.take_profit(), entry_price=self.buy_stop())
                self._active = False
            return hit
        if self.sell_stop():
            hit = price < self.take_profit()
            if hit:
                if self._active:
                    self.calculate_profit(exit_price=self.take_profit(), entry_price=self.sell_stop())
                self._active = False
            return hit
        return False
    
    def __str__(self):
        return f'Trade(\n' + \
            f'  symbol={self.symbol()}' + \
            f'  timeframe={self.timeframe()}' + \
            f'  buy_stop={self.buy_stop()}\n' + \
            f'  sell_stop={self.sell_stop()}\n' + \
            f'  stop_loss={self.stop_loss()}\n' + \
            f'  take_profit={self.take_profit()}\n' + \
            f'  active={self.active()}\n' + \
        ')' \
            