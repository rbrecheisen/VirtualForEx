import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

from matplotlib.dates import num2date

from PySide6.QtWidgets import (
    QVBoxLayout,
    QMessageBox,
)

from virtualforex.ui.panels.panel import Panel
from virtualforex.ui.components.figurecanvas import FigureCanvas
from virtualforex.ui.components.navigationtoolbar import NavigationToolbar
from virtualforex.core.pricedata import PriceData
from virtualforex.core.trade import Trade
from virtualforex.core.tradehistory import TradeHistory


class PriceChartPanel(Panel):
    NONE = 0
    BUY_STOP = 1
    SELL_STOP = 2
    STOP_LOSS = 3
    TAKE_PROFIT = 4

    def __init__(self):
        super(PriceChartPanel, self).__init__()
        self._canvas = None
        self._canvas_figure = None
        self._chart = None
        self._navigation_toolbar = None
        self._price_data = None
        self._cid = None
        self._click_state = None
        self._current_trade = None
        self._lines = []
        self.init_layout()

    # GET/SET

    def canvas(self):
        if not self._canvas:
            self._canvas = FigureCanvas(self.canvas_figure())
            self._cid = self._canvas.mpl_connect('button_press_event', self.on_click)
        return self._canvas
    
    def canvas_figure(self):
        return self._canvas_figure
    
    def set_canvas_figure(self, canvas_figure):
        self._canvas_figure = canvas_figure

    def chart(self):
        return self._chart
    
    def set_chart(self, chart):
        self._chart = chart
    
    def navigation_toolbar(self):
        if not self._navigation_toolbar:
            self._navigation_toolbar = NavigationToolbar(self.canvas(), self)
        return self._navigation_toolbar
    
    def price_data(self):
        return self._price_data

    def set_price_data(self, price_data):
        self._price_data = price_data
        self.update_chart(self._price_data.first_n(PriceData.DEFAULT_PAGE_SIZE))

    def page_size(self):
        if self.price_data():
            return self.price_data().page_size()
    
    def set_page_size(self, page_size):
        if self.price_data():
            self.price_data().set_page_size(page_size)

    def click_state(self):
        return self._click_state

    def set_click_state(self, click_state):
        self._click_state = click_state

    def current_trade(self):
        return self._current_trade
    
    def create_new_current_trade(self):
        self._current_trade = Trade()

    def save_current_trade(self):
        pass

    def lines(self):
        return self._lines

    # LAYOUT

    def init_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.navigation_toolbar())
        layout.addWidget(self.canvas())
        self.setLayout(layout)

    # UTILITY

    def show_all_candles(self):
        if self.price_data():
            self.update_chart(self.price_data().all())

    def show_prev_candle(self):
        if self.current_trade():
            QMessageBox.information(self, 'Info', 'When a trade is open, you cannot go back')
            return
        if self.price_data():
            self.update_chart(self.price_data().prev())

    def show_prev_candle_page(self):
        if self.current_trade():
            QMessageBox.information(self, 'Info', 'When a trade is open, you cannot go back')
        if self.price_data():
            self.update_chart(self.price_data().prev_page())

    def show_next_candle(self):
        if self.price_data():
            self.update_chart(self.price_data().next())
            if self.current_trade():
                last_bar = self.price_data().last_bar()
                if self.current_trade().buy_stop():
                    if self.current_trade().buy_stop_hit(last_bar.high()):
                        print(f'Buy stop was hit at {self.current_trade().buy_stop()}')
                    if self.current_trade().stop_loss_hit(last_bar.low()):
                        print(f'Stop loss for BUY order was hit at {self.current_trade().stop_loss()}')
                        print(f'   Profit in euros: {self.current_trade().profit()}')
                        # self.lines().clear()
                        # self.update_chart(self.price_data().current())
                    if self.current_trade().take_profit_hit(last_bar.high()):
                        print(f'Take profit level for BUY order was hit at {self.current_trade().take_profit()}')
                        print(f'   Profit in euros: {self.current_trade().profit()}')
                        # self.lines().clear()
                        # self.update_chart(self.price_data().current())
                elif self.current_trade().sell_stop():
                    if self.current_trade().sell_stop_hit(last_bar.low()):
                        print(f'Sell stop was hit at {self.current_trade().sell_stop()}')
                    if self.current_trade().stop_loss_hit(last_bar.high()):
                        print(f'Stop loss for SELL order was hit at {self.current_trade().stop_loss()}')
                        print(f'   Profit in euros: {self.current_trade().profit()}')
                        # self.lines().clear()
                        # self.update_chart(self.price_data().current())
                    if self.current_trade().take_profit_hit(last_bar.low()):
                        print(f'Take profit level for SELL order was hit at {self.current_trade().take_profit()}')
                        print(f'   Profit in euros: {self.current_trade().profit()}')
                        # self.lines().clear()
                        # self.update_chart(self.price_data().current())

    def show_next_candle_page(self):
        if self.current_trade():
            QMessageBox.information(self, 'Info', 'When a trade is open, you cannot move forward a whole page')
        if self.price_data():
            self.update_chart(self.price_data().next_page())

    def jump_to_date(self, new_date):
        if self.price_data():
            self.update_chart(self.price_data().jump_to_date(new_date))

    def update_chart(self, data):
        plt.close(self.canvas_figure())
        # Make sure to set show_nontrading=True, otherwise the click event.xdata will not match the Matplotlib ticks
        figure, axlist = mpf.plot(
            data, type='candle', style='yahoo', returnfig=True, title=self.price_data().name(), show_nontrading=True)
        self.set_canvas_figure(figure)
        self.set_chart(axlist[0])
        for label in self.chart().get_xticklabels():
            label.set_rotation(90)
        # Redraw any lines
        for line in self.lines():
            self.draw_line(line['price'], line['color'], line['label'])
        self.layout().removeWidget(self.canvas())
        self.layout().removeWidget(self.navigation_toolbar())
        self.navigation_toolbar().setParent(None)
        self.canvas().setParent(None)
        if self._cid:
            self.canvas().mpl_disconnect(self._cid)
        self._navigation_toolbar = None
        self._canvas = None
        self.layout().addWidget(self.navigation_toolbar())
        self.layout().addWidget(self.canvas())

    def draw_line(self, price, color, label):
        xmin = self.chart().get_xlim()[0]
        self.chart().axhline(y=price, color=color, linestyle='--', linewidth=1.2)
        self.chart().text(xmin, price, label, color=color, fontsize=9, verticalalignment='bottom', horizontalalignment='left', backgroundcolor='white', clip_on=True)
        self.canvas().draw()

    # EVENTS

    def on_click(self, event):
        if self.navigation_toolbar().mode != '':
            return
        if event.inaxes:
            # event.button: 1=left, 2=middle, 3=right
            # replace timezone info from matplotlib date otherwise it cannot be compared
            # to the datetime index of our price data
            date = pd.Timestamp(num2date(event.xdata).replace(tzinfo=None))
            button = event.button
            price = event.ydata
            if button == 1:
                if self.current_trade():
                    if self.click_state() == PriceChartPanel.BUY_STOP:
                        color, label = 'blue', 'Buy Stop'
                        self.draw_line(price, color, label)
                        self.lines().append({'price': price, 'color': color, 'label': label})
                        self.current_trade().set_buy_stop(price)
                    elif self.click_state() == PriceChartPanel.SELL_STOP:
                        color, label = 'blue', 'Sell Stop'
                        self.draw_line(price, color, label)
                        self.lines().append({'price': price, 'color': color, 'label': label})
                        self.current_trade().set_sell_stop(price)
                    elif self.click_state() == PriceChartPanel.STOP_LOSS:
                        color, label = 'red', 'Stop Loss'
                        self.draw_line(price, color, label)
                        self.lines().append({'price': price, 'color': color, 'label': label})
                        self.current_trade().set_stop_loss(price)
                    elif self.click_state() == PriceChartPanel.TAKE_PROFIT:
                        color, label = 'green', 'Take Profit'
                        self.draw_line(price, color, label)
                        self.lines().append({'price': price, 'color': color, 'label': label})
                        self.current_trade().set_take_profit(price)
                print(f'date: {date}, price: {price}')
            if button == 3:
                self.jump_to_date(date)
