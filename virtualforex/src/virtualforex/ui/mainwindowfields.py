from virtualforex.ui.maindockwidget import MainDockWidget
from virtualforex.ui.sidedockwidget import SideDockWidget


class MainWindowFields:
    def __init__(self, main_window):
        self._main_window = main_window
        self._main_dockwidget = None
        self._side_dockwidget = None

    def main_window(self):
        return self._main_window
    
    def main_dockwidget(self):
        if not self._main_dockwidget:
            self._main_dockwidget = MainDockWidget(self.main_window())
        return self._main_dockwidget
    
    def side_dockwidget(self):
        if not self._side_dockwidget:
            self._side_dockwidget = SideDockWidget(self.main_window())
        return self._side_dockwidget