import sys

from PySide6 import QtWidgets

from rbeesoft.ui.settings import Settings

from virtualforex.ui.constants import Constants
from virtualforex.ui.mainwindow import MainWindow
from virtualforex.ui.components.splashscreen import SplashScreen
from virtualforex.ui.utils import resource_path, version


def main():
    settings = Settings()
    application_name = settings.get(Constants.VIRTUALFOREX_NAME)
    QtWidgets.QApplication.setApplicationName(application_name)
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(application_name)
    main_window = MainWindow(
        Constants.VIRTUALFOREX_WINDOW_TITLE, application_name, version(), None)
    splash_screen = SplashScreen(main_window)
    splash_screen.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()