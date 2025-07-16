from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QDockWidget,
)

from virtualforex.ui.pricechartcontrols import PriceChartControls


class SideDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super(SideDockWidget, self).__init__(parent)
        self._price_chart_controls = None
        self.init_layout()
        self.setObjectName('sidedockwidget')

    # GET/SET

    def price_chart_controls(self):
        if not self._price_chart_controls:
            self._price_chart_controls = PriceChartControls()
        return self._price_chart_controls

    # LAYOUT
        
    def init_layout(self):
        self.setWindowTitle('Price chart controls')
        layout = QVBoxLayout()
        layout.addWidget(self.price_chart_controls())
        container = QWidget()
        container.setLayout(layout)
        self.setWidget(container)