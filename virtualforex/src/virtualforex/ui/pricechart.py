from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMessageBox,
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
        self._canvas = None
        self._navigation_toolbar = None
        self._trader = None
        self._button_pressed = None
        self._delta = None
        self._selected_line = None
        self._current_line_type = None
        self._current_trade = None
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
            # self._price_data_window.first_page()
            self._price_data_window.random_page()
        return self._price_data_window

    def canvas(self):
        if not self._canvas:
            self._canvas = FigureCanvas()
            self._canvas.mpl_connect('button_press_event', self.on_click)
        return self._canvas
    
    def navigation_toolbar(self):
        if not self._navigation_toolbar:
            self._navigation_toolbar = NavigationToolbar(self.canvas())
        return self._navigation_toolbar
    
    def trader(self):
        if not self._trader:
            self._trader = Trader()
        return self._trader
    
    def current_trade(self):
        return self._current_trade
    
    def set_current_trade(self, trade):
        self._current_trade = trade
    
    def button_pressed(self):
        if not self._button_pressed:
            self._button_pressed = False
        return self._button_pressed
    
    def set_button_pressed(self, button_pressed):
        self._button_pressed = button_pressed

    def current_line_type(self):
        return self._current_line_type
    
    def set_current_line_type(self, current_line_type):
        self._current_line_type = current_line_type

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
            # self.price_data_window().first_page()
            self.update_chart()

    def calculate_stop_loss_updated(self, new_calculate_stop_loss):
        self.trader().set_calculate_stop_loss(new_calculate_stop_loss)

    def line_type_changed(self, new_line_type):
        self.set_current_line_type(new_line_type)

    # TRADING
    
    def buy(self):
        self.set_current_trade(None)
        message = 'You are starting a BUY trade.\n'
        message += 'The trade will become active as soon as you place a buy stop.\n'
        message += 'In that case, you can only advance the chart one candle at a time.'
        QMessageBox.information(self, 'Information', message)

    def sell(self):
        self.set_current_trade(None)
        message = 'You are starting a SELL trade.\n'
        message += 'The trade will become active as soon as you place a sell stop.\n'
        message += 'In that case, you can only advance the chart one candle at a time.'
        QMessageBox.information(self, 'Information', message)

    # NAVIGATION

    def next(self):
        if self.price_data():
            self.price_data_window().next()
            self.update_chart()
            if self.current_trade():
                last_bar = self.price_data_window().last_bar()
                if self.current_trade().triggered_stop(last_bar):
                    # QMessageBox.information(self, 'Information', 'Stop triggered!')
                    print(f'Stop triggered at {self.current_trade().price()}')
                elif self.current_trade().triggered_stop_loss(last_bar):
                    # QMessageBox.information(self, 'Information', 'Stop loss triggered!')
                    print(f'Stop loss triggered at {self.current_trade().stop_loss()}')
                elif self.current_trade().triggered_take_profit(last_bar):
                    # QMessageBox.information(self, 'Information', 'Take profit triggered!')
                    print(f'Take profit triggered at {self.current_trade().take_profit()}')
                else:
                    pass

    def next_page(self):
        if self.current_trade():
            QMessageBox.warning(self, 'Warning', 'You can only step forward while trading')
            return
        if self.price_data():
            self.price_data_window().next_page()
            self.update_chart()

    def prev(self):
        if self.current_trade():
            QMessageBox.warning(self, 'Warning', 'You can only step forward while trading')
            return
        if self.price_data():
            self.price_data_window().prev()
            self.update_chart()

    def prev_page(self):
        if self.current_trade():
            QMessageBox.warning(self, 'Warning', 'You can only step forward while trading')
            return
        if self.price_data():
            self.price_data_window().prev_page()
            self.update_chart()

    def first_page(self):
        if self.current_trade():
            QMessageBox.warning(self, 'Warning', 'You can only step forward while trading')
            return
        if self.price_data():
            self.price_data_window().first_page()
            self.update_chart()

    def last_page(self):
        if self.current_trade():
            QMessageBox.warning(self, 'Warning', 'You can only step forward while trading')
            return
        if self.price_data():
            self.price_data_window().last_page()
            self.update_chart()

    def reset(self):
        if self.current_trade():
            QMessageBox.warning(self, 'Warning', 'You cannot reset chart while trading')
            return
        if self.price_data():
            self.price_data_window().reset()
            self.update_chart()

    # MOUSE EVENTS

    def on_click(self, event):
        if self.price_data() and event.inaxes:
            self.set_button_pressed(False)
            price = event.ydata
            if event.button == 1:
                if self.current_line_type() == 'Buy Stop':
                    if not self.current_trade():
                        self.add_line(price, 'green', 'Buy Stop')
                        self.set_current_trade(self.trader().buy(price))
                        if self.trader().calculate_stop_loss():
                            self.add_line(self.current_trade().stop_loss(), 'red', 'Stop Loss')                        

                elif self.current_line_type() == 'Sell Stop':
                    if not self.current_trade():
                        self.add_line(price, 'green', 'Sell Stop')
                        self.set_current_trade(self.trader().sell(price))
                        if self.trader().calculate_stop_loss():
                            self.add_line(self.current_trade().stop_loss(), 'red', 'Stop Loss')

                elif self.current_line_type() == 'Stop Loss':
                    if self.current_trade():
                        self.add_line(price, 'red', 'Stop Loss')
                        self.current_trade().set_stop_loss(price)

                elif self.current_line_type() == 'Take Profit':
                    if self.current_trade():
                        self.add_line(price, 'orange', 'Take Profit')
                        self.current_trade().set_take_profit(price)

                else:
                    QMessageBox.warning(self, 'Warning', 'Select line type before you click')
            else:
                return
            
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