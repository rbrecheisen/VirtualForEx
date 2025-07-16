import mplfinance as mpf
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class FigureCanvas(FigureCanvasQTAgg):
    def __init__(self):
        super(FigureCanvas, self).__init__(Figure())
        # self.mpl_connect('button_press_event', self.on_click)
        self._axes = None
        self._lines = []

    # GET/SET

    def axes(self):
        return self._axes
    
    def lines(self):
        return self._lines
    
    # RENDERING

    def add_line(self, price, color, label):
        self.lines().append({'price': price, 'color': color, 'label': label})

    def remove_line(self, price):
        idx = -1
        for i in range(len(self.lines())):
            if price == self.lines()[i]['price']:
                idx = i
                break
        if idx >= 0:
            self.lines().pop(idx)

    def find_line_between(self, min, max):
        for i in range(len(self.lines())):
            price = self.lines()[i]['price']
            if min <= price <= max:
                return self.lines()[i]
        return None

    def clear_lines(self):
        self.lines().clear()

    def plot(self, df, symbol, timeframe):
        if self.figure:
            self.figure.clear()
            title = f'{symbol} ({timeframe})'
            self._axis = self.figure.add_subplot(111)
            mpf.plot(df, type='candle', style='yahoo', returnfig=False, ax=self._axis, show_nontrading=True)
            self._axis.set_title(title)
            for label in self._axis.get_xticklabels():
                label.set_rotation(90)
            xmin = self._axis.get_xlim()[0]
            for line_info in self.lines():
                self._axis.axhline(
                    y=line_info['price'], color=line_info['color'], linestyle='--', linewidth=1.2)
                self._axis.text(xmin, line_info['price'], line_info['label'], color=line_info['color'], fontsize=9, verticalalignment='bottom', horizontalalignment='left', backgroundcolor='white', clip_on=True)
            self.figure.tight_layout()
            self.draw()

    # HELPERS

    def clear(self):
        if self.figure:
            self.figure.clear()

    def close(self):
        if self.figure:
            plt.close(self.figure)