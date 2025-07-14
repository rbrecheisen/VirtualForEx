import mplfinance as mpf

from PySide6.QtWidgets import (
    QVBoxLayout,
)

from virtualforex.ui.panels.panel import Panel
from virtualforex.ui.components.figurecanvas import FigureCanvas
from virtualforex.ui.components.navigationtoolbar import NavigationToolbar


class PriceChartPanel(Panel):
    def __init__(self):
        super(PriceChartPanel, self).__init__()
        self.set_title('Price chart')
        self._canvas = None
        self._canvas_figure = None
        self._main_axis = None
        self._navigation_toolbar = None
        self._df = None
        self.init_layout()

    def canvas(self):
        if not self._canvas:
            self._canvas = FigureCanvas(self.canvas_figure())
        return self._canvas
    
    def canvas_figure(self):
        return self._canvas_figure

    def main_axis(self):
        return self._main_axis
    
    def navigation_toolbar(self):
        if not self._navigation_toolbar:
            self._navigation_toolbar = NavigationToolbar(self.canvas(), self)
        return self._navigation_toolbar
    
    def init_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.navigation_toolbar())
        layout.addWidget(self.canvas())
        self.setLayout(layout)

    def set_data(self, df, name=None):
        self._df = df
        self._canvas_figure, axlist = mpf.plot(self._df, type='candle', style='yahoo', returnfig=True, title=name)
        self._main_axis = axlist[0]
        self.layout().removeWidget(self.canvas())
        self.layout().removeWidget(self.navigation_toolbar())
        self.navigation_toolbar().setParent(None)
        self.canvas().setParent(None)
        self._navigation_toolbar = None
        self._canvas = None
        self.layout().addWidget(self.navigation_toolbar())
        self.layout().addWidget(self.canvas())
