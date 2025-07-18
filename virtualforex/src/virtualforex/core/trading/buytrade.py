from virtualforex.core.trading.trade import Trade


class BuyTrade(Trade):
    def __init__(self, price, stop_loss=None, take_profit=None):
        super(BuyTrade, self).__init__()
        self._price = price
        self._stop_loss = stop_loss
        self._take_profit = take_profit
        self._active = False

    def price(self):
        return self._price
    
    def set_price(self, price):
        self._price = price
    
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
    
    def set_active(self, active):
        self._active = active

    def triggered_stop(self, bar):
        if bar.high() > self.price() and not self.active():
            self.set_active(True)
            return True
        return False
    
    def triggered_stop_loss(self, bar):
        if bar.low() < self.stop_loss() and self.active():
            self.set_active(False)
            return True
        return False
    
    def triggered_take_profit(self, bar):
        if bar.high() > self.take_profit() and self.active():
            self.set_active(False)
            return True
        return False
    
    def __str__(self):
        return f'BuyTrade(price={self.price()}, stop_loss={self.stop_loss()}, take_profit={self.take_profit()})'