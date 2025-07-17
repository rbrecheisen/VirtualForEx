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
from virtualforex.core.trading.trader import Trader
from virtualforex.core.utils.logmanager import LogManager

LOG = LogManager()


class PriceChart(QWidget, PriceChartControlsListener):
    def __init__(self, parent=None):
        super(PriceChart, self).__init__(parent)
        self._price_data = None
        self._price_data_window = None
        self._canvas = None
        self._navigation_toolbar = None
        self._trader = None
        self._button_pressed = None
        self._delta = None
        self._selected_line = None
        self.init_layout()

    # GET/SET

    def price_data(self):
        return self._price_data

    def set_price_data(self, price_data):
        self._price_data = price_data
        self.update_chart()

    def price_data_window(self):
        if not self._price_data_window:
            self._price_data_window = PriceDataWindow(self.price_data())
            self._price_data_window.first_page()
        return self._price_data_window

    def canvas(self):
        if not self._canvas:
            self._canvas = FigureCanvas()
            self._canvas.mpl_connect('button_press_event', self.on_click)
            self._canvas.mpl_connect('button_release_event', self.on_release)
            self._canvas.mpl_connect('motion_notify_event', self.on_move)
        return self._canvas
    
    def navigation_toolbar(self):
        if not self._navigation_toolbar:
            self._navigation_toolbar = NavigationToolbar(self.canvas())
        return self._navigation_toolbar
    
    def trader(self):
        if not self._trader:
            self._trader = Trader()
        return self._trader
    
    def button_pressed(self):
        if not self._button_pressed:
            self._button_pressed = False
        return self._button_pressed
    
    def set_button_pressed(self, button_pressed):
        self._button_pressed = button_pressed

    def delta(self):
        if not self._delta:
            self._delta = 0.05
        return self._delta
    
    def set_delta(self, delta):
        self._delta = delta

    def selected_line(self):
        return self._selected_line
    
    def set_selected_line(self, selected_line):
        self._selected_line = selected_line
        
    # LAYOUT

    def init_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.navigation_toolbar())
        layout.addWidget(self.canvas())
        self.setLayout(layout)

    # EVENT HANDLERS

    def account_size_updated(self, new_account_size):
        self.trader().set_account_size(new_account_size)

    def lot_size_updated(self, new_lot_size):
        self.trader().set_lot_size(new_lot_size)
    
    def leverage_updated(self, new_leverage):
        pass
    
    def risk_updated(self, new_risk):
        self.trader().set_risk(new_risk)

    def pip_updated(self, new_pip):
        self.trader().set_pip(new_pip)
    
    def page_size_updated(self, new_page_size):
        if self.price_data():
            self.price_data_window().set_page_size(new_page_size)
            self.price_data_window().first_page()
            self.update_chart()

    # TRADING
    
    def buy(self):
        pass

    def sell(self):
        pass

    # NAVIGATION

    def next(self):
        self.price_data_window().next()
        self.update_chart()

    def next_page(self):
        self.price_data_window().next_page()
        self.update_chart()

    def prev(self):
        self.price_data_window().prev()
        self.update_chart()

    def prev_page(self):
        self.price_data_window().prev_page()
        self.update_chart()

    def first_page(self):
        self.price_data_window().first_page()
        self.update_chart()

    def last_page(self):
        self.price_data_window().last_page()
        self.update_chart()

    def reset(self):
        self.price_data_window().reset()
        self.update_chart()

    # MOUSE EVENTS

    def on_click(self, event):
        if self.price_data() and event.inaxes:
            self.set_button_pressed(False)
            price = event.ydata
            if event.button == 1:
                line = self.find_line_between(price-self.delta(), price+self.delta())
                if not line:
                    # This is a new line. Depending on the line type, a buy/sell stop should be placed
                    # or a take profit point. The stop loss is calculated automatically.
                    self.add_line(price, 'green', 'Buy Stop')
                else:
                    # User selected existing line, so he can move it
                    self.set_selected_line(line)
                    self.set_button_pressed(True)
            elif event.button == 3:
                line = self.find_line_between(price-self.delta(), price+self.delta())
                if line:
                    self.remove_line(line['price'])
            else:
                return
            
    def on_release(self, event):
        if self.price_data() and event.inaxes:
            self.set_selected_line(None)
            self.set_button_pressed(False)

    def on_move(self, event):
        if self.price_data() and event.inaxes:
            if self.button_pressed():
                self.selected_line()['price'] = event.ydata
                self.update_chart()

    # RENDERING

    def find_line_between(self, min, max):
        return self.canvas().find_line_between(min, max)

    def add_line(self, price, color, label):
        self.canvas().add_line(price, color, label)
        self.update_chart()

    def remove_line(self, price):
        self.canvas().remove_line(price)
        self.update_chart()

    def clear_lines(self):
        self.canvas().clear_lines()
        self.update_chart()

    def update_chart(self):
        if self.price_data():
            self.canvas().plot(
                self.price_data_window().current_page(), 
                self.price_data().symbol(), 
                self.price_data().timeframe()
            )