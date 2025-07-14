import sys
import pandas as pd
import numpy as np
import mplfinance as mpf

from matplotlib.dates import num2date

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

START_DATE = "2024-10-01"
END_DATE = "2025-02-01"
STYLE=  'yahoo'


# https://chatgpt.com/c/68739930-54d8-800b-8b00-57fa886b9ea9
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mplfinance + PySide6 + Click Events")
        self._toolbar = None
        self._fig = None
        self._main_ax = None
        self._canvas = None
        self.setCentralWidget(QWidget())
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar())
        layout.addWidget(self.canvas())
        self.centralWidget().setLayout(layout)
        self.cid = self.canvas().mpl_connect('button_press_event', self.on_click)
        self.lines = []

    def canvas(self):
        if not self._canvas:
            self._canvas = FigureCanvas(self.fig())
        return self._canvas

    def toolbar(self):
        if not self._toolbar:
            self._toolbar = NavigationToolbar(self.canvas(), self)
        return self._toolbar

    def fig(self):
        df = pd.read_csv("G:\\My Drive\\data\\MetaTrader5\\EURUSD_D1.csv", parse_dates=['Date'])
        df.set_index('Date', inplace=True)
        filtered_df = df.loc[START_DATE:END_DATE]
        fig, axlist = mpf.plot(filtered_df, type='candle', style='yahoo', returnfig=True, show_nontrading=True)
        self._main_ax = axlist[0]  # Candlestick plot is in the first axis
        return fig
    
    def main_ax(self):
        return self._main_ax

    def on_click(self, event):
        if self.toolbar().mode != '':
            return
        if event.inaxes == self.main_ax():
            from datetime import datetime
            y = event.ydata
            print(f"Clicked at price: {y:.2f}, date: {num2date(event.xdata, tz=datetime.now().astimezone().tzinfo)}")
            line = self.main_ax().axhline(y=y, color='green', linestyle='--', linewidth=1.2)
            self.lines.append(line)
            self.canvas().draw()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1000, 700)
    window.show()
    app.exec()


if __name__ == '__main__':
    main()