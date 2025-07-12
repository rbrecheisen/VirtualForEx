from rbeesoft.ui.mainwindow import MainWindow as BaseMainWindow

from virtualforex.ui.components.graphicsview import GraphicsView


class MainWindow(BaseMainWindow):
    def __init__(self, title, app_name, version, icon):
        super(MainWindow, self).__init__(title, app_name, version, icon)
        self._graphics_view = None
        self.init_layout()

    def graphics_view(self):
        if not self._graphics_view:
            self._graphics_view = GraphicsView()
        return self._graphics_view

    def init_layout(self):
        self.setCentralWidget(self.graphics_view())