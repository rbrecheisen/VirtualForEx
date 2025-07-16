from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QDockWidget,
)

from virtualforex.ui.pricechart import PriceChart


class MainDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super(MainDockWidget, self).__init__(parent)
        self._price_chart = None
        self.init_layout()
        self.setObjectName('maindockwidget')

    # GET/SET

    def price_chart(self):
        if not self._price_chart:
            self._price_chart = PriceChart(self)
        return self._price_chart

    def init_layout(self):
        self.setWindowTitle('Price chart')
        layout = QVBoxLayout()
        layout.addWidget(self.price_chart())
        container = QWidget()
        container.setLayout(layout)
        self.setWidget(container)