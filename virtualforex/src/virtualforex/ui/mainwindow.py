from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QSpinBox,
    QLabel,
)
from PySide6.QtGui import (
    QAction,
)
from PySide6.QtCore import Qt

from rbeesoft.ui.mainwindow import MainWindow as BaseMainWindow
from virtualforex.ui.panels.stackedpanel import StackedPanel
from virtualforex.ui.panels.pricechartpanel import PriceChartPanel
from virtualforex.ui.dialogs.loadpricedatadialog import LoadPriceDataDialog
from virtualforex.core.pricedata import PriceData


class MainWindow(BaseMainWindow):
    def __init__(self, title, app_name, version, icon):
        super(MainWindow, self).__init__(title, app_name, version, icon)
        self._price_chart_panel = None
        self._main_panel = None
        self._prev_candle_button = None
        self._prev_candle_page_button = None
        self._next_candle_button = None
        self._next_candle_page_button = None
        self._last_candle_button = None
        self._page_size_spinbox = None
        self._line_type_combobox = None
        self.init_layout()

    # GET/SET

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
    
    def prev_candle_button(self):
        if not self._prev_candle_button:
            self._prev_candle_button = QPushButton('<', self)
            self._prev_candle_button.setToolTip('Key = A')
            self._prev_candle_button.setStyleSheet('color: white; background-color: green; font-weight: bold;')
            self._prev_candle_button.clicked.connect(self.handle_prev_candle_button)
        return self._prev_candle_button
    
    def prev_candle_page_button(self):
        if not self._prev_candle_page_button:
            self._prev_candle_page_button = QPushButton('<<', self)
            self._prev_candle_page_button.setToolTip('Key = PageUp')
            self._prev_candle_page_button.setStyleSheet('color: white; background-color: green; font-weight: bold;')
            self._prev_candle_page_button.clicked.connect(self.handle_prev_candle_page_button)
        return self._prev_candle_page_button
    
    def next_candle_button(self):
        if not self._next_candle_button:
            self._next_candle_button = QPushButton('>', self)
            self._next_candle_button.setToolTip('Key = D')
            self._next_candle_button.setStyleSheet('color: white; background-color: green; font-weight: bold;')
            self._next_candle_button.clicked.connect(self.handle_next_candle_button)
        return self._next_candle_button
    
    def next_candle_page_button(self):
        if not self._next_candle_page_button:
            self._next_candle_page_button = QPushButton('>>', self)
            self._next_candle_page_button.setToolTip('Key = PageDown')
            self._next_candle_page_button.setStyleSheet('color: white; background-color: green; font-weight: bold;')
            self._next_candle_page_button.clicked.connect(self.handle_next_candle_page_button)
        return self._next_candle_page_button
    
    def page_size_spinbox(self):
        if not self._page_size_spinbox:
            self._page_size_spinbox = QSpinBox(minimum=10, maximum=500)
            self._page_size_spinbox.valueChanged.connect(self.handle_page_size_spinbox)
            self._page_size_spinbox.setValue(PriceData.DEFAULT_PAGE_SIZE)
        return self._page_size_spinbox
    
    def line_type_combobox(self):
        if not self._line_type_combobox:
            self._line_type_combobox = QComboBox()
            self._line_type_combobox.addItems([None, 'Buy Stop', 'Sell Stop', 'Stop Loss', 'Take Profit'])
            self._line_type_combobox.currentTextChanged.connect(self.handle_line_type_combobox)
        return self._line_type_combobox
    
    # LAYOUT
    
    def init_layout(self):
        self.init_menus()
        self.setCentralWidget(QWidget())
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_candle_page_button())
        button_layout.addWidget(self.prev_candle_button())
        button_layout.addWidget(self.next_candle_button())
        button_layout.addWidget(self.next_candle_page_button())
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(QLabel('Page size:'))
        layout.addWidget(self.page_size_spinbox())
        layout.addWidget(QLabel('Line type:'))
        layout.addWidget(self.line_type_combobox())
        layout.addWidget(self.main_panel())
        self.centralWidget().setLayout(layout)

    def init_menus(self):
        self.init_data_menu()
        self.init_view_menu()

    def init_data_menu(self):
        load_price_data_action = QAction('Load price data...', self)
        load_price_data_action.triggered.connect(self.handle_load_price_data_action)
        menu = self.menuBar().addMenu('Data')
        menu.addAction(load_price_data_action)

    def init_view_menu(self):
        show_all_candles_action = QAction('Show all candles', self)
        show_all_candles_action.triggered.connect(self.handle_show_all_candles_action)
        menu = self.menuBar().addMenu('View')
        menu.addAction(show_all_candles_action)

    # EVENTS

    def handle_load_price_data_action(self):
        dialog = LoadPriceDataDialog()
        result = dialog.exec()
        if result:
            self.price_chart_panel().set_price_data(dialog.price_data())

    def handle_show_all_candles_action(self):
        self.price_chart_panel().show_all_candles()

    def handle_prev_candle_button(self):
        self.price_chart_panel().show_prev_candle()

    def handle_prev_candle_page_button(self):
        self.price_chart_panel().show_prev_candle_page()

    def handle_next_candle_button(self):
        self.price_chart_panel().show_next_candle()

    def handle_next_candle_page_button(self):
        self.price_chart_panel().show_next_candle_page()

    def handle_page_size_spinbox(self, new_value):
        self.price_chart_panel().set_page_size(new_value)

    def handle_line_type_combobox(self, text):
        if text == 'Buy Stop':
            self.price_chart_panel().set_click_state(PriceChartPanel.BUY_STOP)
        elif text == 'Sell Stop':
            self.price_chart_panel().set_click_state(PriceChartPanel.SELL_STOP)
        elif text == 'Stop Loss':
            self.price_chart_panel().set_click_state(PriceChartPanel.STOP_LOSS)
        elif text == 'Take Profit':
            self.price_chart_panel().set_click_state(PriceChartPanel.TAKE_PROFIT)
        else:
            self.price_chart_panel().set_click_state(None)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.handle_prev_candle_page_button()
        elif event.key() == Qt.Key_PageDown:
            self.handle_next_candle_page_button()
        elif event.key() == Qt.Key_A:
            self.handle_prev_candle_button()
        elif event.key() == Qt.Key_D:
            self.handle_next_candle_button()
        else:
            return super().keyPressEvent(event)