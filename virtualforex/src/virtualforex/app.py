import sys

from PySide6 import QtWidgets

from rbeesoft.ui.settings import Settings
from rbeesoft.ui.utils import resource_path, version

from virtualforex.ui.constants import Constants
from virtualforex.ui.mainwindow import MainWindow


def main():
    settings = Settings()
    application_name = settings.get(Constants.VIRTUALFOREX_NAME)
    QtWidgets.QApplication.setApplicationName(application_name)
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(application_name)
    # THIS DOESN"T WORK
    version_file_path = resource_path(f'{application_name}/src/{application_name}/resources/VERSION')
    main_window = MainWindow(
        Constants.VIRTUALFOREX_WINDOW_TITLE, 
        application_name, 
        version(version_file_path), 
        None
    )
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()