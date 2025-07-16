from virtualforex.core.trading.buytrade import BuyTrade
from virtualforex.core.trading.buystoplosscalculator import BuyStopLossCalculator
from virtualforex.core.trading.selltrade import SellTrade
from virtualforex.core.trading.sellstoplosscalculator import SellStopLossCalculator


class Trader:
    def __init__(self, account_size, lot_size, risk, pip=0.0001):
        self._account_size = account_size
        self._lot_size = lot_size
        self._risk = risk
        self._pip = pip

    # GET/SET

    def account_size(self):
        return self._account_size
    
    def lot_size(self):
        return self._lot_size
    
    def risk(self):
        return self._risk
    
    def pip(self):
        return self._pip
    
    # TRADING

    def buy(self, price, take_profit):
        calculator = BuyStopLossCalculator(self.account_size(), self.lot_size(), self.risk(), self.pip())
        stop_loss = calculator.calculate(price)
        return BuyTrade(price, stop_loss, take_profit)
    
    def sell(self, price, take_profit):
        calculator = SellStopLossCalculator(self.account_size(), self.lot_size(), self.risk(), self.pip())
        stop_loss = calculator.calculate(price)
        return SellTrade(price, stop_loss, take_profit)
