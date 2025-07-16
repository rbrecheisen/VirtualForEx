import os
import json


class TradeHistory:
    def __init__(self):
        self._trades = self.load_trades_from_json()

    def trades(self):
        return self._trades

    def load_trades_from_json(self):
        return []
    
    def save_trades_to_json(self):
        pass

    def add_trade(self, trade):
        self.trades().append(trade)