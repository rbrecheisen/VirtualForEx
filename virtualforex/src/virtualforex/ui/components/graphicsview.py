from PySide6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,
)
from PySide6.QtGui import (
    QWheelEvent,
    QMouseEvent,
    QPainter,
    QColor,
)
from PySide6.QtCore import (
    Qt,
    QRectF,
    QPointF,
)


class GraphicsView(QGraphicsView):
    def __init__(self):
        super(GraphicsView, self).__init__()
        self._scene = None
        self._scene_item = None
        self._panning = None
        self._last_mouse_position = None
        self._last_mouse_anchor_position = None
        self.init_view()

    # GET/SET

    def scene_item(self):
        if not self._scene_item:
            self._scene_item = QGraphicsEllipseItem(QRectF(50, 50, 100, 100))
            self._scene_item.setBrush(QColor(200, 200, 200))
        return self._scene_item

    def panning(self):
        if not self._panning:
            self._panning = False
        return self._panning
    
    def set_panning(self, panning):
        self._panning = panning
    
    def last_mouse_position(self):
        if not self._last_mouse_position:
            self._last_mouse_position = QPointF()
        return self._last_mouse_position
    
    def set_last_mouse_position(self, last_mouse_position):
        self._last_mouse_position = last_mouse_position

    # INITIALIZATION

    def init_view(self):
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        # self.setDragMode(QGraphicsView.NoDrag)
        # self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scene = QGraphicsScene(self)
        scene.setSceneRect(-10000, -10000, 20000, 20000)
        scene.addItem(self.scene_item())
        self.setScene(scene)

    # EVENT HANDLERS

    def wheelEvent(self, event):
        zoom_factor = 1.15
        old_pos = self.mapToScene(event.position().toPoint())
        if event.angleDelta().y() > 0:
            self.scale(zoom_factor, zoom_factor)
        else:
            self.scale(1/zoom_factor, 1/zoom_factor)
        new_pos = self.mapToScene(event.position().toPoint())
        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.modifiers() == Qt.ShiftModifier:
            self.set_panning(True)
            self.set_last_mouse_position(event.position())
            self.setCursor(Qt.ClosedHandCursor)
        else:
            return super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        if self.panning():
            delta = event.position() - self.last_mouse_position()
            self.set_last_mouse_position(event.position())
            self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
            # self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
            self.translate(delta.x(), delta.y())
            # self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        else:
            return super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.panning():
            self.set_panning(False)
            self.setCursor(Qt.ArrowCursor)
        else:
            return super().mouseReleaseEvent(event)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self.resetTransform()
            self.centerOn(self.scene_item())
        else:
            super().keyPressEvent(event)
        
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