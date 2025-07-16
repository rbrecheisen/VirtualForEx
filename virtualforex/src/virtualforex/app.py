import sys
import traceback

from PySide6 import QtWidgets

from rbeesoft.ui.settings import Settings
from virtualforex.ui.mainwindow import MainWindow


def main():
    settings = Settings()
    application_name = settings.get('virtualforex')
    QtWidgets.QApplication.setApplicationName(application_name)
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(application_name)
    try:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(str(e))
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()