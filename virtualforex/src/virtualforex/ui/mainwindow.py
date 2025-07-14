from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
)
from PySide6.QtGui import (
    QAction,
)

from rbeesoft.ui.mainwindow import MainWindow as BaseMainWindow
from virtualforex.ui.panels.stackedpanel import StackedPanel
from virtualforex.ui.panels.pricechartpanel import PriceChartPanel
from virtualforex.ui.dialogs.loadpricedatadialog import LoadPriceDataDialog


class MainWindow(BaseMainWindow):
    def __init__(self, title, app_name, version, icon):
        super(MainWindow, self).__init__(title, app_name, version, icon)
        self._price_chart_panel = None
        self._main_panel = None
        self.init_menus()
        self.init_layout()

    def price_chart_panel(self):
        if not self._price_chart_panel:
            self._price_chart_panel = PriceChartPanel()
        return self._price_chart_panel
    
    def main_panel(self):
        if not self._main_panel:
            self._main_panel = StackedPanel()
            self._main_panel.add_panel(self.price_chart_panel(), 'price_chart')
            self._main_panel.switch_to('price_chart')
        return self._main_panel
    
    def init_menus(self):
        load_price_data_action = QAction('Load price data...', self)
        load_price_data_action.triggered.connect(self.handle_load_price_data_action)
        menu = self.menuBar().addMenu('Data')
        menu.addAction(load_price_data_action)

    def init_layout(self):
        self.setCentralWidget(QWidget())
        layout = QVBoxLayout()
        layout.addWidget(self.main_panel())
        self.centralWidget().setLayout(layout)

    def handle_load_price_data_action(self):
        dialog = LoadPriceDataDialog()
        result = dialog.exec()
        if result:
            data = dialog.data()
            name = f'{dialog.symbol_name()} ({dialog.timeframe()})'
            self.price_chart_panel().set_data(data, name)