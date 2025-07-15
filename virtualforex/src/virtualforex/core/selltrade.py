from virtualforex.core.abstracttrade import AbstractTrade


class SellTrade(AbstractTrade):
    def __init__(self, sell_stop, stop_loss, take_profit):
        self._sell_stop = sell_stop
        self._stop_loss = stop_loss
        self._take_profit = take_profit