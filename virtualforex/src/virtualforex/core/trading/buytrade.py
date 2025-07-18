from virtualforex.core.trading.trade import Trade


class BuyTrade(Trade):
    def __init__(self, price, stop_loss, take_profit=None):
        super(BuyTrade, self).__init__()
        self._price = price
        self._stop_loss = stop_loss
        self._take_profit = take_profit

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
    
    def __str__(self):
        return f'BuyTrade(price={self.price()}, stop_loss={self.stop_loss()}, take_profit={self.take_profit()})'