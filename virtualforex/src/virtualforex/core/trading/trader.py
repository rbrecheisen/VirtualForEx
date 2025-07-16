from virtualforex.core.trading.buytrade import BuyTrade
from virtualforex.core.trading.buystoplosscalculator import BuyStopLossCalculator
from virtualforex.core.trading.selltrade import SellTrade
from virtualforex.core.trading.sellstoplosscalculator import SellStopLossCalculator


class Trader:
    def __init__(self):
        self._account_size = 0
        self._lot_size = 0
        self._risk = 0
        self._pip = 0.0001

    # GET/SET

    def account_size(self):
        return self._account_size
    
    def set_account_size(self, account_size):
        self._account_size = account_size
    
    def lot_size(self):
        return self._lot_size
    
    def set_lot_size(self, lot_size):
        self._lot_size = lot_size
    
    def risk(self):
        return self._risk
    
    def set_risk(self, risk):
        self._risk = risk
    
    def pip(self):
        return self._pip
    
    def set_pip(self, pip):
        self._pip = pip
    
    # TRADING

    def buy(self, price, take_profit):
        if not self.account_size() or not self.lot_size() or not self.risk() or not self.pip():
            raise RuntimeError('Trade not yet configured')
        calculator = BuyStopLossCalculator(self.account_size(), self.lot_size(), self.risk(), self.pip())
        stop_loss = calculator.calculate(price)
        return BuyTrade(price, stop_loss, take_profit)
    
    def sell(self, price, take_profit):
        if not self.account_size() or not self.lot_size() or not self.risk() or not self.pip():
            raise RuntimeError('Trade not yet configured')
        calculator = SellStopLossCalculator(self.account_size(), self.lot_size(), self.risk(), self.pip())
        stop_loss = calculator.calculate(price)
        return SellTrade(price, stop_loss, take_profit)
