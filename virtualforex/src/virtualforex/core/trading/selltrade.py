from virtualforex.core.trading.trade import Trade


class SellTrade(Trade):
    def __init__(self, price, stop_loss, take_profit):
        super(SellTrade, self).__init__()
        self._price = price
        self._stop_loss = stop_loss
        self._take_profit = take_profit

    def price(self):
        return self._price
    
    def stop_loss(self):
        return self._stop_loss
    
    def take_profit(self):
        return self._take_profit
    
    def __str__(self):
        return f'SellTrade(price={self.price()}, stop_loss={self.stop_loss()}, take_profit={self.take_profit()})'