import mplfinance as mpf
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class FigureCanvas(FigureCanvasQTAgg):
    def __init__(self):
        super(FigureCanvas, self).__init__(Figure())
        self._axes = None

    def axes(self):
        return self._axes

    def plot(self, df, symbol, timeframe):
        self.clear()
        title = f'{symbol} ({timeframe})'
        self.figure, axlist = mpf.plot(
            df, type='candle', style='yahoo', returnfig=True, title=title, show_nontrading=True)
        self._axes = axlist[0]

    def clear(self):
        if self.figure:
            self.figure.clear()
    
    def close(self):
        if self.figure:
            plt.close(self.figure)