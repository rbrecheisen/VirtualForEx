class Trade:
    def __init__(self):
        self._symbol = None
        self._timeframe = None
        self._buy_stop = None
        self._sell_stop = None
        self._stop_loss = None
        self._take_profit = None
        self._active = False
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
        self._buy_stop = buy_stop

    def sell_stop(self):
        return self._sell_stop
    
    def set_sell_stop(self, sell_stop):
        self._sell_stop = sell_stop

    def stop_loss(self):
        return self._stop_loss
    
    def set_stop_loss(self, stop_loss):
        self._stop_loss = stop_loss

    def take_profit(self):
        return self._take_profit
    
    def set_take_profit(self, take_profit):
        self._take_profit = take_profit

    def bars(self):
        return self._bars

    # HELPERS

    def add_bar(self, bar):
        self.bars().append(bar)

    def is_active(self):
        return self._active

    def buy_stop_hit(self, price):
        if self.buy_stop():
            hit = price > self.buy_stop()
            if hit:
                self._active = True
            return hit
        raise RuntimeError('No buy stop set')
    
    def sell_stop_hit(self, price):
        if self.sell_stop():
            hit = price < self.sell_stop()
            if hit:
                self._active = True
            return hit
        raise RuntimeError('No sell stop set')

    def stop_loss_hit(self, price):
        if self.buy_stop():
            hit = price < self.stop_loss()
            if hit:
                self._active = False
            return hit
        if self.sell_stop():
            hit = price > self.stop_loss()
            if hit:
                self._active = False
            return hit
        raise RuntimeError('No buy or sell stop set')
    
    def take_profit_hit(self, price):
        if self.buy_stop():
            hit = price > self.take_profit()
            if hit:
                self._active = False
            return hit
        if self.sell_stop():
            hit = price < self.take_profit()
            if hit:
                self._active = False
            return hit
        raise RuntimeError('No buy or sell stop set')