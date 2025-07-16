from PySide6.QtWidgets import QSizePolicy

from virtualforex.ui.components.spacer import Spacer


class VerticalSpacer(Spacer):
    def __init__(self):
        super(VerticalSpacer, self).__init__()
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)