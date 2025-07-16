from PySide6.QtWidgets import QDialog


class Dialog(QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)