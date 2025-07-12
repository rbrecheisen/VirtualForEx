from PySide6.QtCore import Qt, QRectF, QPoint, QStandardPaths, Signal
from PySide6.QtGui import QPixmap, QBrush, QColor, QCursor
from PySide6.QtWidgets import (
    QApplication, QWidget, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsItem,
    QFrame, QLabel, QPushButton, QGridLayout, QFileDialog, QMessageBox
)

SCALE_FACTOR = 1.25


class PriceBar:
    def __init__(self, open_price, close_price, low_price, high_price):
        self._open_price = open_price
        self._close_price = close_price
        self._low_price = low_price
        self._high_price = high_price


class PriceBarSequenceModel:
    def __init__(self, bars):
        self._bars = bars
        self._visible_index = 0

    def next_bar(self):
        if self._visible_index < len(self._bars):
            self._visible_index += 1

    def visible_bars(self):
        return self._bars[:self._visible_index]
    

class PriceBarGraphicsItem(QGraphicsItem):
    def __init__(self, bar, x_position):
        super(PriceBarGraphicsItem, self).__init__()
        self._bar = bar
        self._x_position = x_position

    def boundingRect(self):
        return QRectF(self._x_position, 0, 5, 100)
    
    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(Qt.blue))
        painter.drawEllipse(self.boundingRect())


class InteractiveGraphicsView(QGraphicsView):
    # coordinatesChanged = Signal(QPoint)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._zoom = 0
        self._pinned = False
        self._scene = QGraphicsScene(self)

        self._price_bar_sequence_model = PriceBarSequenceModel([
            PriceBar(10, 20, 5, 25),
            PriceBar(10, 20, 5, 25),
            PriceBar(10, 20, 5, 25),
            PriceBar(10, 20, 5, 25),
        ])

        self.setScene(self._scene)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QBrush(QColor(255, 255, 255)))
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.resetView()

    def render_bars(self):
        self._scene.clear()
        for i, bar in enumerate(self._price_bar_sequence_model.visible_bars()):
            item = PriceBarGraphicsItem(bar, x_position=i*10)
            self._scene.addItem(item)

    def next_bar(self):
        self._price_bar_sequence_model.next_bar()
        self.render_bars()

    def resetView(self, scale=1):
        rect = QRectF(-500, -500, 1000, 1000)
        self.setSceneRect(rect)
        self._zoom = 0
        unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
        self.scale(1 / unity.width(), 1 / unity.height())
        viewrect = self.viewport().rect()
        scenerect = self.transform().mapRect(rect)
        factor = min(viewrect.width() / scenerect.width(),
                     viewrect.height() / scenerect.height()) * scale
        self.scale(factor, factor)
        # self.centerOn(self._price_bar)
        self.updateCoordinates()

    def zoom(self, step):
        zoom = max(0, self._zoom + (step := int(step)))
        if zoom != self._zoom:
            self._zoom = zoom
            if self._zoom > 0:
                factor = SCALE_FACTOR ** step if step > 0 else 1 / SCALE_FACTOR ** abs(step)
                self.scale(factor, factor)
            else:
                self.resetView()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.zoom(delta and delta // abs(delta))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resetView()

    def updateCoordinates(self, pos=None):
        if pos is None:
            pos = self.mapFromGlobal(QCursor.pos())
        point = self.mapToScene(pos).toPoint()
        # self.coordinatesChanged.emit(point)

    def mouseMoveEvent(self, event):
        self.updateCoordinates(event.position().toPoint())
        super().mouseMoveEvent(event)

    def drawBackground(self, painter, rect):
        painter.save()
        painter.setPen(QColor(230, 230, 230))
        grid_size = 100
        left = int(rect.left()) - (int(rect.left()) % grid_size)
        top = int(rect.top()) - (int(rect.top()) % grid_size)
        for x in range(left, int(rect.right()), grid_size):
            painter.drawLine(x, rect.top(), x, rect.bottom())
        for y in range(top, int(rect.bottom()), grid_size):
            painter.drawLine(rect.left(), y, rect.right(), y)
        painter.restore()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self._viewer = InteractiveGraphicsView(self)
        button = QPushButton('Next', self)
        button.clicked.connect(self.handle_button)
        layout = QGridLayout(self)
        layout.addWidget(self._viewer, 0, 0, 1, 3)
        layout.addWidget(button, 1, 0, 1, 1)
        layout.setColumnStretch(2, 2)
        self._path = None

    def handle_button(self):
        self._viewer.next_bar()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 800, 600)
    window.show()
    sys.exit(app.exec())
