class SellStopLossCalculator:
    def __init__(self, account_size, lot_size, risk, pip=0.0001):
        self._account_size = account_size
        self._lot_size = lot_size
        self._risk = risk
        self._pip = pip

    def account_size(self):
        return self._account_size

    def lot_size(self):
        return self._lot_size
    
    def risk(self):
        return self._risk
    
    def pip(self):
        return self._pip
    
    def pip_price(self):
        return self.lot_size() * self.pip()
    
    def calculate(self, price):
        risk_in_euros = self.account_size() * self.risk()
        risk_in_other_currency = risk_in_euros * price
        nr_pips = risk_in_other_currency * self.pip_price()
        stop_loss = price + nr_pips * self.pip()
        return stop_loss