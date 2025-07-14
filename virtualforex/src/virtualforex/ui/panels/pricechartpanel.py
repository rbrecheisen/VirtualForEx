import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

from matplotlib.dates import num2date

from PySide6.QtWidgets import (
    QVBoxLayout,
)

from virtualforex.ui.panels.panel import Panel
from virtualforex.ui.components.figurecanvas import FigureCanvas
from virtualforex.ui.components.navigationtoolbar import NavigationToolbar


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
        self.update_chart(self._price_data.all())

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
        if self.price_data():
            self.update_chart(self.price_data().prev())

    def show_prev_candle_page(self):
        if self.price_data():
            self.update_chart(self.price_data().prev_page())

    def show_next_candle(self):
        if self.price_data():
            self.update_chart(self.price_data().next())

    def show_next_candle_page(self):
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
                if self.click_state() == PriceChartPanel.BUY_STOP:
                    self.draw_line(price, 'blue', 'Buy Stop')
                elif self.click_state() == PriceChartPanel.SELL_STOP:
                    self.draw_line(price, 'blue', 'Sell Stop')
                elif self.click_state() == PriceChartPanel.STOP_LOSS:
                    self.draw_line(price, 'red', 'Stop Loss')
                elif self.click_state() == PriceChartPanel.TAKE_PROFIT:
                    self.draw_line(price, 'green', 'Take Profit')
                else:
                    print(f'date: {date}, price: {price}')
            if button == 3:
                self.jump_to_date(date)
