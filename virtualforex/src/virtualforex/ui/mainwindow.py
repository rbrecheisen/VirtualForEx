from PySide6.QtGui import (
    QAction,
)
from PySide6.QtCore import Qt

from rbeesoft.ui.mainwindow import MainWindow as BaseMainWindow
from virtualforex.ui.maindockwidget import MainDockWidget
from virtualforex.ui.sidedockwidget import SideDockWidget
from virtualforex.ui.loadpricedatadialog import LoadPriceDataDialog


class MainWindow(BaseMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__('VirtualFX', 'virtualfx', '1.0', None)
        self._main_dockwidget = None
        self._side_dockwidget = None
        self.init_layout()

    # GET/SET

    def main_dockwidget(self):
        if not self._main_dockwidget:
            self._main_dockwidget = MainDockWidget(self)
        return self._main_dockwidget
    
    def side_dockwidget(self):
        if not self._side_dockwidget:
            self._side_dockwidget = SideDockWidget(self)
            self._side_dockwidget.price_chart_controls().add_listener(self.main_dockwidget().price_chart())
        return self._side_dockwidget
    
    # LAYOUT
    
    def init_layout(self):
        self.init_data_menu()
        self.setWindowTitle('VirtualFX')
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.main_dockwidget())
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.side_dockwidget())

    def init_data_menu(self):
        load_price_data_action = QAction('Load price data...', self)
        load_price_data_action.triggered.connect(self.handle_load_price_data_action)
        data_menu = self.menuBar().addMenu('Data')
        data_menu.addAction(load_price_data_action)

    # EVENTS

    def handle_load_price_data_action(self):
        dialog = LoadPriceDataDialog()
        result = dialog.exec()
        if result:
            price_data = dialog.price_data()
            self.main_dockwidget().price_chart().set_price_data(price_data)
