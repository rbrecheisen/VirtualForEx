from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QPushButton,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QLabel,
    QMessageBox,
)

from virtualforex.ui.components.verticalspacer import VerticalSpacer


class PriceChartControls(QWidget):
    def __init__(self):
        super(PriceChartControls, self).__init__()
        self._account_size_spinbox = None
        self._lot_size_combobox = None
        self._leverage_spinbox = None
        self._risk_spinbox = None
        self._pip_combobox = None
        self._page_size_combobox = None
        self._update_button = None
        self._buy_button = None
        self._sell_button = None
        self._line_type_label = None
        self._line_type_combobox = None
        self._clear_lines_button = None
        self._next_button = None
        self._next_page_button = None
        self._prev_button = None
        self._prev_page_button = None
        self._first_page_button = None
        self._last_page_button = None
        self._reset_button = None
        self._listeners = []
        self.init_layout()

    # GET/SET

    def account_size_spinbox(self):
        if not self._account_size_spinbox:
            self._account_size_spinbox = QSpinBox(self, minimum=0, maximum=100000, value=1000)
        return self._account_size_spinbox

    def lot_size_combobox(self):
        if not self._lot_size_combobox:
            self._lot_size_combobox = QComboBox(self)
            self._lot_size_combobox.addItems(['10000', '100000'])
        return self._lot_size_combobox
    
    def leverage_spinbox(self):
        if not self._leverage_spinbox:
            self._leverage_spinbox = QSpinBox(self, minimum=30, maximum=100, value=30)
        return self._leverage_spinbox
    
    def risk_spinbox(self):
        if not self._risk_spinbox:
            self._risk_spinbox = QSpinBox(self, minimum=0, maximum=100, value=2)
        return self._risk_spinbox
    
    def pip_combobox(self):
        if not self._pip_combobox:
            self._pip_combobox = QComboBox()
            self._pip_combobox.addItems(['0.0001', '0.001'])
        return self._pip_combobox
    
    def page_size_combobox(self):
        if not self._page_size_combobox:
            self._page_size_combobox = QComboBox(self)
            self._page_size_combobox.addItems(['100', '50'])
        return self._page_size_combobox
    
    def update_button(self):
        if not self._update_button:
            self._update_button = QPushButton('Update', self)
            self._update_button.clicked.connect(self.handle_update_button)
        return self._update_button
    
    def buy_button(self):
        if not self._buy_button:
            self._buy_button = QPushButton('Buy', self)
            self._buy_button.setStyleSheet('QPushButton:checked {background-color: green; color: white;}')
            self._buy_button.clicked.connect(self.handle_buy_button)
            self._buy_button.setCheckable(True)
        return self._buy_button
    
    def sell_button(self):
        if not self._sell_button:
            self._sell_button = QPushButton('Sell', self)
            self._sell_button.setStyleSheet('QPushButton:checked {background-color: red; color: white;}')
            self._sell_button.clicked.connect(self.handle_sell_button)
            self._sell_button.setCheckable(True)
        return self._sell_button
    
    def line_type_label(self):
        if not self._line_type_label:
            self._line_type_label = QLabel('Select line type:')
            self._line_type_label.setStyleSheet('font-weight: bold;')
        return self._line_type_label
    
    def line_type_combobox(self):
        if not self._line_type_combobox:
            self._line_type_combobox = QComboBox(self)
            self._line_type_combobox.addItems([None, 'Buy Stop', 'Sell Stop', 'Take Profit'])
            self._line_type_combobox.setEnabled(False)
        return self._line_type_combobox
    
    def clear_lines_button(self):
        if not self._clear_lines_button:
            self._clear_lines_button = QPushButton('Clear lines', self)
            self._clear_lines_button.clicked.connect(self.handle_clear_lines_button)
        return self._clear_lines_button
    
    def next_button(self):
        if not self._next_button:
            self._next_button = QPushButton('>', self)
            self._next_button.setToolTip('Move to next candle')
            self._next_button.clicked.connect(self.handle_next_button)
        return self._next_button
    
    def next_page_button(self):
        if not self._next_page_button:
            self._next_page_button = QPushButton('>>', self)
            self._next_page_button.setToolTip('Move to next page')
            self._next_page_button.clicked.connect(self.handle_next_page_button)
        return self._next_page_button

    def prev_button(self):
        if not self._prev_button:
            self._prev_button = QPushButton('<', self)
            self._prev_button.setToolTip('Move to previous candle')
            self._prev_button.clicked.connect(self.handle_prev_button)
        return self._prev_button
    
    def prev_page_button(self):
        if not self._prev_page_button:
            self._prev_page_button = QPushButton('<<', self)
            self._prev_page_button.setToolTip('Move to previous page')
            self._prev_page_button.clicked.connect(self.handle_prev_page_button)
        return self._prev_page_button

    def first_page_button(self):
        if not self._first_page_button:
            self._first_page_button = QPushButton('|<<', self)
            self._first_page_button.setToolTip('Move to first page')
            self._first_page_button.clicked.connect(self.handle_first_page_button)
        return self._first_page_button

    def last_page_button(self):
        if not self._last_page_button:
            self._last_page_button = QPushButton('>>|', self)
            self._last_page_button.setToolTip('Move to last page')
            self._last_page_button.clicked.connect(self.handle_last_page_button)
        return self._last_page_button
    
    def reset_button(self):
        if not self._reset_button:
            self._reset_button = QPushButton('Reset chart', self)
            self._reset_button.clicked.connect(self.handle_reset_button)
        return self._reset_button

    # LAYOUT

    def init_layout(self):
        form_layout = QFormLayout()
        form_layout.addRow('Account size', self.account_size_spinbox())
        form_layout.addRow('Lot size', self.lot_size_combobox())
        form_layout.addRow('Leverage', self.leverage_spinbox())
        form_layout.addRow('Risk (%)', self.risk_spinbox())
        form_layout.addRow('Pip', self.pip_combobox())
        form_layout.addRow('Page size', self.page_size_combobox())
        trade_buttons_layout = QHBoxLayout()
        trade_buttons_layout.addWidget(self.buy_button())
        trade_buttons_layout.addWidget(self.sell_button())
        navigation_buttons_layout = QHBoxLayout()
        navigation_buttons_layout.addWidget(self.prev_page_button())
        navigation_buttons_layout.addWidget(self.prev_button())
        navigation_buttons_layout.addWidget(self.next_button())
        navigation_buttons_layout.addWidget(self.next_page_button())
        first_last_buttons_layout = QHBoxLayout()
        first_last_buttons_layout.addWidget(self.first_page_button())
        first_last_buttons_layout.addWidget(self.last_page_button())
        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.update_button())
        layout.addWidget(self.clear_lines_button())
        layout.addLayout(trade_buttons_layout)
        layout.addWidget(QLabel('Select line type:'))
        layout.addWidget(self.line_type_combobox())
        layout.addWidget(QLabel('Navigation:'))
        layout.addLayout(navigation_buttons_layout)
        layout.addLayout(first_last_buttons_layout)
        layout.addWidget(self.reset_button())
        layout.addWidget(VerticalSpacer())
        self.setLayout(layout)

    # LISTENERS

    def add_listener(self, listener):
        if listener not in self._listeners:
            self._listeners.append(listener)

    def notify_account_size_updated(self, new_account_size):
        for listener in self._listeners:
            listener.account_size_updated(new_account_size)

    def notify_lot_size_updated(self, new_lot_size):
        for listener in self._listeners:
            listener.lot_size_updated(new_lot_size)

    def notify_leverage_updated(self, new_leverage):
        for listener in self._listeners:
            listener.leverage_updated(new_leverage)

    def notify_risk_updated(self, new_risk):
        for listener in self._listeners:
            listener.risk_updated(new_risk)

    def notify_pip_updated(self, new_pip):
        for listener in self._listeners:
            listener.pip_updated(new_pip)

    def notify_page_size_updated(self, new_page_size):
        for listener in self._listeners:
            listener.page_size_updated(new_page_size)

    def notify_clear_lines(self):
        for listener in self._listeners:
            listener.clear_lines()

    def notify_buy(self):
        for listener in self._listeners:
            listener.buy()

    def notify_sell(self):
        for listener in self._listeners:
            listener.sell()

    def notify_next(self):
        for listener in self._listeners:
            listener.next()

    def notify_next_page(self):
        for listener in self._listeners:
            listener.next_page()

    def notify_prev(self):
        for listener in self._listeners:
            listener.prev()

    def notify_prev_page(self):
        for listener in self._listeners:
            listener.prev_page()

    def notify_first_page(self):
        for listener in self._listeners:
            listener.first_page()

    def notify_last_page(self):
        for listener in self._listeners:
            listener.last_page()

    def notify_reset(self):
        for listener in self._listeners:
            listener.reset()

    # EVENTS

    def handle_update_button(self):
        if self.buy_button().isChecked() or self.sell_button().isChecked():
            QMessageBox.warning(self, 'Warning', 'Trade in progress! Close it first before updating parameters.')
            return
        self.notify_account_size_updated(self.account_size_spinbox().value())
        self.notify_lot_size_updated(int(self.lot_size_combobox().currentText()))
        self.notify_leverage_updated(self.leverage_spinbox().value())
        self.notify_risk_updated(float(self.risk_spinbox().value() / 100.0))
        self.notify_pip_updated(float(self.pip_combobox().currentText()))
        self.notify_page_size_updated(int(self.page_size_combobox().currentText()))

    def handle_buy_button(self):
        if self.sell_button().isChecked():
            self.buy_button().setChecked(False)
            QMessageBox.warning(self, 'Warning', 'Sell trade already active! Close it first.')
            return
        self.line_type_combobox().setEnabled(self.buy_button().isChecked())
        if self.buy_button().isChecked():
            self.notify_buy()

    def handle_sell_button(self):
        if self.buy_button().isChecked():
            self.sell_button().setChecked(False)
            QMessageBox.warning(self, 'Warning', 'Buy trade already active! Close it first.')
            return
        self.line_type_combobox().setEditable(self.sell_button().isChecked())
        if self.sell_button().isChecked():
            self.notify_sell()

    def handle_clear_lines_button(self):
        self.notify_clear_lines()

    def handle_next_button(self):
        self.notify_next()

    def handle_next_page_button(self):
        self.notify_next_page()

    def handle_prev_button(self):
        self.notify_prev()

    def handle_prev_page_button(self):
        self.notify_prev_page()

    def handle_first_page_button(self):
        self.notify_first_page()

    def handle_last_page_button(self):
        self.notify_last_page()

    def handle_reset_button(self):
        self.notify_reset()