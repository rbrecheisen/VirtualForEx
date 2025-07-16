from PySide6.QtWidgets import QWidget


class Panel(QWidget):
    def __init__(self):
        super(Panel, self).__init__()
        self._title = None

    def title(self):
        if not self._title:
            raise RuntimeError('Panel title not set')
        return self._title
    
    def set_title(self, title):
        self._title = title