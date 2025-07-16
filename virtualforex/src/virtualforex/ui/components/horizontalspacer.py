from PySide6.QtWidgets import QSizePolicy

from virtualforex.ui.components.spacer import Spacer


class HorizontalSpacer(Spacer):
    def __init__(self):
        super(HorizontalSpacer, self).__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)