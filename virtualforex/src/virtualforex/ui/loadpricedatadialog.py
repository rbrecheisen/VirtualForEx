import os
import pandas as pd

from PySide6.QtWidgets import (
    QFormLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QLabel,
    QDialog,
    QCalendarWidget,
)
from PySide6.QtCore import QDate

from virtualforex.ui.settings import Settings
from virtualforex.core.data.pricedata import PriceData

CALENDAR_STYLESHEET = 'QCalendarWidget QAbstractItemView::item:selected {background-color: #0078d7; color: white; border-radius: 4px;}'


class LoadPriceDataDialog(QDialog):
    def __init__(self, parent=None):
        super(LoadPriceDataDialog, self).__init__(parent)
        self._file_path_line_edit = None
        self._file_path_select_button = None
        self._start_date_calendar_widget = None
        self._end_date_calendar_widget = None
        self._symbol_name_label = None
        self._timeframe_label = None
        self._ok_button = None
        self._cancel_button = None
        self._settings = None
        self._price_data = None
        self.init_layout()

    # GET/SET

    def file_path_line_edit(self):
        if not self._file_path_line_edit:
            self._file_path_line_edit = QLineEdit()
        return self._file_path_line_edit
    
    def file_path_select_button(self):
        if not self._file_path_select_button:
            self._file_path_select_button = QPushButton('Select', self)
            self._file_path_select_button.clicked.connect(self.handle_file_path_select_button)
        return self._file_path_select_button
    
    def start_date_calendar_widget(self):
        if not self._start_date_calendar_widget:
            self._start_date_calendar_widget = QCalendarWidget(self)
            self._start_date_calendar_widget.setStyleSheet(CALENDAR_STYLESHEET)
        return self._start_date_calendar_widget
    
    def end_date_calendar_widget(self):
        if not self._end_date_calendar_widget:
            self._end_date_calendar_widget = QCalendarWidget(self)
            self._end_date_calendar_widget.setStyleSheet(CALENDAR_STYLESHEET)
        return self._end_date_calendar_widget
    
    def symbol_name_label(self):
        if not self._symbol_name_label:
            self._symbol_name_label = QLabel()
        return self._symbol_name_label
    
    def symbol_name(self):
        return self._symbol_name_label.text()
    
    def timeframe_label(self):
        if not self._timeframe_label:
            self._timeframe_label = QLabel()
        return self._timeframe_label
    
    def timeframe(self):
        return self._timeframe_label.text()
    
    def ok_button(self):
        if not self._ok_button:
            self._ok_button = QPushButton('Ok', self)
            self._ok_button.clicked.connect(self.accept)
        return self._ok_button
    
    def cancel_button(self):
        if not self._cancel_button:
            self._cancel_button = QPushButton('Cancel', self)
            self._cancel_button.clicked.connect(self.reject)
        return self._cancel_button
    
    def settings(self):
        if not self._settings:
            self._settings = Settings()
        return self._settings
    
    def price_data(self):
        return self._price_data
    
    def set_price_data(self, price_data):
        self._price_data = price_data

    # UTILITY

    def to_q_date(self, date):
        return QDate(date.year, date.month, date.day)
    
    def symbol_name_and_timeframe(self, file_path):
        file_name_no_ext = os.path.split(file_path)[1]
        file_name_no_ext = os.path.splitext(file_name_no_ext)[0]
        items = file_name_no_ext.split('_')
        return items[0], items[1]

    # LAYOUT

    def init_layout(self):
        file_path_layout = QHBoxLayout()
        file_path_layout.addWidget(self.file_path_line_edit())
        file_path_layout.addWidget(self.file_path_select_button())
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button())
        button_layout.addWidget(self.cancel_button())
        form_layout = QFormLayout()
        form_layout.addRow('Symbol name:', self.symbol_name_label())
        form_layout.addRow('Timeframe:', self.timeframe_label())
        form_layout.addRow('File path:', file_path_layout)
        form_layout.addRow('Start date:', self.start_date_calendar_widget())
        form_layout.addRow('End date:', self.end_date_calendar_widget())
        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.setWindowTitle('Load price data')        

    # UTILITY

    def update_price_data(self, file_path):
        self.file_path_line_edit().setText(file_path)
        symbol_name, timeframe = self.symbol_name_and_timeframe(file_path)
        self.symbol_name_label().setText(symbol_name)
        self.timeframe_label().setText(timeframe)
        if timeframe == 'H4':
            df = pd.read_csv(file_path, parse_dates=['Date'], date_format='%Y.%m.%d %H:%M')
        else:
            df = pd.read_csv(file_path, parse_dates=['Date'], date_format='%Y.%m.%d')
        df = df.set_index('Date', inplace=False)
        price_data = PriceData(df, self.symbol_name(), self.timeframe())
        self.set_price_data(price_data)

    def update_calendars(self):
        self.start_date_calendar_widget().setSelectedDate(self.to_q_date(self.price_data().start_date()))
        self.end_date_calendar_widget().setSelectedDate(self.to_q_date(self.price_data().end_date()))

    # EVENTS

    def handle_file_path_select_button(self):
        last_directory = self.settings().get('last_directory', '.')
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select file path', last_directory)
        if file_path:
            self.update_price_data(file_path)
            self.update_calendars()
            self.settings().set('last_directory', os.path.dirname(file_path))