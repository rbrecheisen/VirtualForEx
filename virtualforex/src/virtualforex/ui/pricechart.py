from PySide6.QtWidgets import (
    QWidget,
)

from virtualforex.ui.components.figurecanvas import FigureCanvas
from virtualforex.ui.components.navigationtoolbar import NavigationToolbar
from virtualforex.ui.pricechartcontrolslistener import PriceChartControlsListener
from virtualforex.core.data.pricedatawindow import PriceDataWindow
from virtualforex.core.trading.trader import Trader
from virtualforex.core.utils.logmanager import LogManager

LOG = LogManager()


class PriceChart(QWidget, PriceChartControlsListener):
    def __init__(self, parent=None):
        super(PriceChart, self).__init__(parent)
        self._price_data = None
        self._price_data_window = None
        self._trader = None

    # GET/SET

    def price_data(self):
        return self._price_data

    def set_price_data(self, price_data):
        self._price_data = price_data

    def price_data_window(self):
        if not self._price_data_window:
            self._price_data_window = PriceDataWindow(self.price_data())
        return self._price_data_window
    
    def trader(self):
        return self._trader
    
    def set_trader(self, trader):
        self._trader = trader

    # EVENTS

    def account_size_updated(self, new_account_size):
        LOG.info(f'PriceChart.account_size_updated() new_account_size = {new_account_size}')
        return super().account_size_updated(new_account_size)

    def lot_size_updated(self, new_lot_size):
        LOG.info(f'PriceChart.lot_size_updated() new_lot_size = {new_lot_size}')
        return super().lot_size_updated(new_lot_size)
    
    def leverage_updated(self, new_leverage):
        LOG.info(f'PriceChart.leverage_updated() new_leverage = {new_leverage}')
        return super().leverage_updated(new_leverage)
    
    def risk_updated(self, new_risk):
        LOG.info(f'PriceChart.risk_updated() new_risk = {new_risk}')
        return super().risk_updated(new_risk)
    
    def page_size_updated(self, new_page_size):
        LOG.info(f'PriceChart.page_size_updated() new_page_size = {new_page_size}')
        return super().page_size_updated(new_page_size)
    
    # RENDERING

    def update_chart(self):
        if self.price_data():
            pass