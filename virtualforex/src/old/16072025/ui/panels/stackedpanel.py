from PySide6.QtWidgets import QStackedWidget

from virtualforex.ui.panels.panel import Panel


class StackedPanel(QStackedWidget):
    def __init__(self):
        super(StackedPanel, self).__init__()
        self._current_panel_name = None
        self._panels = {}

    def add_panel(self, panel, name):
        if not isinstance(panel, Panel):
            raise RuntimeError('Panel must extend from Panel')
        if name not in self._panels.keys():
            self._panels[name] = panel
            self._current_panel_name = name
            self.addWidget(panel)

    def current_panel_name(self):
        return self._current_panel_name

    def switch_to(self, name):
        panel = self._panels[name]
        self._current_panel_name = name
        self.setCurrentWidget(panel)