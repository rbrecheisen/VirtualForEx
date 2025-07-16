from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QPushButton,
    QComboBox,
    QSpinBox,
    QLabel,
    QMessageBox,
)

from virtualforex.ui.components.verticalspacer import VerticalSpacer


class PriceChartControls(QWidget):
    def __init__(self):
        super(PriceChartControls, self).__init__()
        self._account_size_spinbox = None
        self._lot_size_spinbox = None
        self._leverage_spinbox = None
        self._risk_spinbox = None
        self._page_size_combobox = None
        self._update_button = None
        self._buy_button = None
        self._sell_button = None
        self._listeners = []
        self.init_layout()

    # GET/SET

    def account_size_spinbox(self):
        if not self._account_size_spinbox:
            self._account_size_spinbox = QSpinBox(self, minimum=0, maximum=100000, value=1000)
        return self._account_size_spinbox

    def lot_size_spinbox(self):
        if not self._lot_size_spinbox:
            self._lot_size_spinbox = QSpinBox(self, minimum=1000, maximum=100000, value=10000)
        return self._lot_size_spinbox
    
    def leverage_spinbox(self):
        if not self._leverage_spinbox:
            self._leverage_spinbox = QSpinBox(self, minimum=30, maximum=100, value=30)
        return self._leverage_spinbox
    
    def risk_spinbox(self):
        if not self._risk_spinbox:
            self._risk_spinbox = QSpinBox(self, minimum=0, maximum=100, value=2)
        return self._risk_spinbox
    
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

    # LAYOUT

    def init_layout(self):
        form_layout = QFormLayout()
        form_layout.addRow('Account size', self.account_size_spinbox())
        form_layout.addRow('Lot size', self.lot_size_spinbox())
        form_layout.addRow('Leverage', self.leverage_spinbox())
        form_layout.addRow('Risk (%)', self.risk_spinbox())
        form_layout.addRow('Page size', self.page_size_combobox())
        trade_buttons_layout = QHBoxLayout()
        trade_buttons_layout.addWidget(self.buy_button())
        trade_buttons_layout.addWidget(self.sell_button())
        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.update_button())
        layout.addLayout(trade_buttons_layout)
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

    def notify_page_size_updated(self, new_page_size):
        for listener in self._listeners:
            listener.page_size_updated(new_page_size)

    # EVENTS

    def handle_update_button(self):
        self.notify_account_size_updated(self.account_size_spinbox().value())
        self.notify_lot_size_updated(self.lot_size_spinbox().value())
        self.notify_leverage_updated(self.leverage_spinbox().value())
        self.notify_risk_updated(float(self.risk_spinbox().value() / 100.0))
        self.notify_page_size_updated(int(self.page_size_combobox().currentText()))

    def handle_buy_button(self):
        if self.sell_button().isChecked():
            self.buy_button().setChecked(False)
            QMessageBox.warning(self, 'Warning', 'Sell trade already active! Close it first.')

    def handle_sell_button(self):
        if self.buy_button().isChecked():
            self.sell_button().setChecked(False)
            QMessageBox.warning(self, 'Warning', 'Buy trade already active! Close it first.')