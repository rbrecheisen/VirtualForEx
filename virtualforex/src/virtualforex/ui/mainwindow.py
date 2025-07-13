from rbeesoft.ui.mainwindow import MainWindow as BaseMainWindow


class MainWindow(BaseMainWindow):
    def __init__(self, title, app_name, version, icon):
        super(MainWindow, self).__init__(title, app_name, version, icon)
        self.init_layout()

    def init_layout(self):
        pass