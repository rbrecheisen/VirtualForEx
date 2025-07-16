from virtualforex.core.abstracttrade import AbstractTrade


class BuyTrade(AbstractTrade):
    def __init__(self, buy_stop, stop_loss, take_profit):
        self._buy_stop = buy_stop
        self._stop_loss = stop_loss
        self._take_profit = take_profit

    def is_hit(self, bar):
        return False