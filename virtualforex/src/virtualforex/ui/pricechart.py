import mplfinance as mpf

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMessageBox,
)

from virtualforex.ui.components.figurecanvas import FigureCanvas
from virtualforex.ui.components.figure import Figure
from virtualforex.ui.components.navigationtoolbar import NavigationToolbar
from virtualforex.ui.pricechartcontrolslistener import PriceChartControlsListener
from virtualforex.core.data.pricedatawindow import PriceDataWindow
from virtualforex.core.utils.logmanager import LogManager

LOG = LogManager()


class PriceChart(QWidget, PriceChartControlsListener):
    def __init__(self, parent=None):
        super(PriceChart, self).__init__(parent)
        self._price_data = None
        self._canvas = None
        self._navigation_toolbar = None
        self.init_layout()

    # GET/SET

    def price_data(self):
        return self._price_data

    def set_price_data(self, price_data):
        self._price_data = price_data
        self.update_chart()

    def canvas(self):
        if not self._canvas:
            self._canvas = FigureCanvas()
        return self._canvas
    
    def navigation_toolbar(self):
        if not self._navigation_toolbar:
            self._navigation_toolbar = NavigationToolbar(self.canvas())
        return self._navigation_toolbar
        
    # LAYOUT

    def init_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.navigation_toolbar())
        layout.addWidget(self.canvas())
        self.setLayout(layout)

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
            self.canvas().figure.clear()
            ax = self.canvas().figure.add_subplot(111)
            mpf.plot(
                self.price_data().df(), 
                type='candle', 
                style='yahoo', 
                returnfig=False, 
                ax=ax,
                show_nontrading=True
            )
            ax.set_title('EURUSD (D1)')
            self.canvas().figure.tight_layout()
            self.canvas().draw()
